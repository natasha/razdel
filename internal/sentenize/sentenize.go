package sentenize

import (
	"regexp"
	"strings"
	"unicode"

	"github.com/natasha/razdel/internal/base"
	"github.com/natasha/razdel/internal/punct"
	"github.com/natasha/razdel/internal/sokr"
)

// Regular expressions
var (
	spaceSuffixRe  = regexp.MustCompile(`\s$`)
	spacePrefixRe  = regexp.MustCompile(`^\s`)
	tokenRe        = regexp.MustCompile(`([^\W\d]+|\d+|[^\w\s])`)
	firstTokenRe   = regexp.MustCompile(`^\s*([^\W\d]+|\d+|[^\w\s])`)
	lastTokenRe    = regexp.MustCompile(`([^\W\d]+|\d+|[^\w\s])\s*$`)
	wordRe         = regexp.MustCompile(`([^\W\d]+|\d+)`)
	pairSokrRe     = regexp.MustCompile(`(\w)\s*\.\s*(\w)\s*$`)
	intSokrRe      = regexp.MustCompile(`\d+\s*-?\s*(\w+)\s*$`)
	romanRe        = regexp.MustCompile(`^[IVXML]+$`)
	smilePrefixRe  = regexp.MustCompile(`^\s*` + punct.SmilesPattern)
)

const (
	bulletChars = "§абвгдеabcdef"
	bulletBounds = ".)"
	bulletSize  = 20
)

// Delimiters for sentence splitting
var delimiters = punct.Endings + ";" + punct.GenericQuotes + punct.CloseQuotes + punct.CloseBrackets

// SentSplit represents a split point for sentence segmentation
type SentSplit struct {
	*base.Split
}

// RightSpacePrefix checks if right side starts with space
func (ss *SentSplit) RightSpacePrefix() bool {
	return spacePrefixRe.MatchString(ss.Split.Right)
}

// LeftSpaceSuffix checks if left side ends with space
func (ss *SentSplit) LeftSpaceSuffix() bool {
	return spaceSuffixRe.MatchString(ss.Split.Left)
}

// RightToken returns the first token on the right
func (ss *SentSplit) RightToken() string {
	match := firstTokenRe.FindStringSubmatch(ss.Split.Right)
	if len(match) > 1 {
		return match[1]
	}
	return ""
}

// LeftToken returns the last token on the left
func (ss *SentSplit) LeftToken() string {
	match := lastTokenRe.FindStringSubmatch(ss.Split.Left)
	if len(match) > 1 {
		return match[1]
	}
	return ""
}

// LeftPairSokr returns pair abbreviation match
func (ss *SentSplit) LeftPairSokr() (string, string, bool) {
	match := pairSokrRe.FindStringSubmatch(ss.Split.Left)
	if len(match) > 2 {
		return match[1], match[2], true
	}
	return "", "", false
}

// RightWord returns the first word on the right
func (ss *SentSplit) RightWord() string {
	match := wordRe.FindString(ss.Split.Right)
	return match
}

// BufferTokens returns all tokens in buffer
func (ss *SentSplit) BufferTokens() []string {
	return tokenRe.FindAllString(ss.Split.Buffer, -1)
}

// BufferFirstToken returns the first token in buffer
func (ss *SentSplit) BufferFirstToken() string {
	match := firstTokenRe.FindStringSubmatch(ss.Split.Buffer)
	if len(match) > 1 {
		return match[1]
	}
	return ""
}

// SentSplitter splits text at potential sentence boundaries
type SentSplitter struct {
	Pattern string
	Window  int
	re      *regexp.Regexp
}

// NewSentSplitter creates a new SentSplitter
func NewSentSplitter() *SentSplitter {
	pattern := `(` + punct.SmilesPattern + `|[` + regexp.QuoteMeta(delimiters) + `])`
	return &SentSplitter{
		Pattern: pattern,
		Window:  10,
		re:      regexp.MustCompile(pattern),
	}
}

// Split implements the Splitter interface
func (ss *SentSplitter) Split(text string) []interface{} {
	text = strings.TrimSpace(text)
	if text == "" {
		return nil
	}

	matches := ss.re.FindAllStringSubmatchIndex(text, -1)
	var result []interface{}
	previous := 0

	for _, match := range matches {
		start := match[0]
		stop := match[1]
		delimiter := text[start:stop]

		// Add left part
		result = append(result, text[previous:start])

		// Create split
		leftStart := maxInt(0, start-ss.Window)
		rightEnd := minInt(len(text), stop+ss.Window)
		left := text[leftStart:start]
		right := text[stop:rightEnd]

		split := &SentSplit{
			Split: base.NewSplit(left, delimiter, right),
		}
		result = append(result, split)
		previous = stop
	}

	// Add remaining text
	result = append(result, text[previous:])

	return result
}

func maxInt(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func minInt(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// isLowerAlpha checks if token is lowercase alphabetic
func isLowerAlpha(token string) bool {
	if token == "" {
		return false
	}
	for _, r := range token {
		if !unicode.IsLetter(r) || !unicode.IsLower(r) {
			return false
		}
	}
	return true
}

// isSokr checks if token is a valid abbreviation context
func isSokr(token string) bool {
	if token == "" {
		return false
	}
	// Numbers are valid context
	for _, r := range token {
		if unicode.IsDigit(r) {
			continue
		} else {
			goto checkAlpha
		}
	}
	return true

checkAlpha:
	// Non-alpha is valid (punct)
	hasAlpha := false
	for _, r := range token {
		if unicode.IsLetter(r) {
			hasAlpha = true
			break
		}
	}
	if !hasAlpha {
		return true
	}
	// Lowercase alpha is valid
	return isLowerAlpha(token)
}

// Rules for sentence segmentation

// emptySide joins if either side is empty
func emptySide(split base.SplitLike) base.RuleAction {
	ss := split.(*SentSplit)
	if ss.LeftToken() == "" || ss.RightToken() == "" {
		return base.ActionJoin
	}
	return base.NoAction
}

// noSpacePrefix joins if no space before next sentence
func noSpacePrefix(split base.SplitLike) base.RuleAction {
	ss := split.(*SentSplit)
	if !ss.RightSpacePrefix() {
		return base.ActionJoin
	}
	return base.NoAction
}

// lowerRight joins if right side starts with lowercase
func lowerRight(split base.SplitLike) base.RuleAction {
	ss := split.(*SentSplit)
	if isLowerAlpha(ss.RightToken()) {
		return base.ActionJoin
	}
	return base.NoAction
}

// delimiterRight joins if right side starts with delimiter
func delimiterRight(split base.SplitLike) base.RuleAction {
	ss := split.(*SentSplit)
	right := ss.RightToken()

	if punct.ContainsRune(punct.GenericQuotes, rune(right[0])) {
		return base.NoAction
	}

	if punct.ContainsRune(delimiters, rune(right[0])) {
		return base.ActionJoin
	}

	if smilePrefixRe.MatchString(ss.Split.Right) {
		return base.ActionJoin
	}

	return base.NoAction
}

// sokrLeft joins for abbreviations on the left
func sokrLeft(split base.SplitLike) base.RuleAction {
	ss := split.(*SentSplit)
	if ss.Split.Delimiter != "." {
		return base.NoAction
	}

	right := ss.RightToken()

	// Check pair abbreviations
	if a, b, ok := ss.LeftPairSokr(); ok {
		left := [2]string{strings.ToLower(a), strings.ToLower(b)}
		if sokr.HeadPairSokrs[left] {
			return base.ActionJoin
		}
		if sokr.PairSokrs[left] && isSokr(right) {
			return base.ActionJoin
		}
		return base.NoAction
	}

	// Check single abbreviations
	left := strings.ToLower(ss.LeftToken())
	if sokr.HeadSokrs[left] {
		return base.ActionJoin
	}
	if sokr.Sokrs[left] && isSokr(right) {
		return base.ActionJoin
	}

	return base.NoAction
}

// insidePairSokr joins inside pair abbreviations
func insidePairSokr(split base.SplitLike) base.RuleAction {
	ss := split.(*SentSplit)
	if ss.Split.Delimiter != "." {
		return base.NoAction
	}

	left := strings.ToLower(ss.LeftToken())
	right := strings.ToLower(ss.RightToken())
	pair := [2]string{left, right}

	if sokr.PairSokrs[pair] {
		return base.ActionJoin
	}

	return base.NoAction
}

// initialsLeft joins for initials
func initialsLeft(split base.SplitLike) base.RuleAction {
	ss := split.(*SentSplit)
	if ss.Split.Delimiter != "." {
		return base.NoAction
	}

	left := ss.LeftToken()
	if len(left) == 1 {
		for _, r := range left {
			if unicode.IsUpper(r) {
				return base.ActionJoin
			}
		}
	}

	if sokr.Initials[strings.ToLower(left)] {
		return base.ActionJoin
	}

	return base.NoAction
}

// closeBound handles closing boundaries
func closeBound(split base.SplitLike) base.RuleAction {
	ss := split.(*SentSplit)
	left := ss.LeftToken()
	if punct.ContainsRune(punct.Endings, rune(left[0])) {
		return base.NoAction
	}
	return base.ActionJoin
}

// closeQuote handles closing quotes
func closeQuote(split base.SplitLike) base.RuleAction {
	ss := split.(*SentSplit)
	delimiter := ss.Split.Delimiter

	if !punct.ContainsRune(punct.Quotes, rune(delimiter[0])) {
		return base.NoAction
	}

	if punct.ContainsRune(punct.CloseQuotes, rune(delimiter[0])) {
		return closeBound(split)
	}

	if punct.ContainsRune(punct.GenericQuotes, rune(delimiter[0])) {
		if !ss.LeftSpaceSuffix() {
			return closeBound(split)
		}
		return base.ActionJoin
	}

	return base.NoAction
}

// closeBracket handles closing brackets
func closeBracket(split base.SplitLike) base.RuleAction {
	ss := split.(*SentSplit)
	if punct.ContainsRune(punct.CloseBrackets, rune(ss.Split.Delimiter[0])) {
		return closeBound(split)
	}
	return base.NoAction
}

// isBullet checks if token is a bullet character
func isBullet(token string) bool {
	if token == "" {
		return false
	}

	// Check if it's a number
	isNum := true
	for _, r := range token {
		if !unicode.IsDigit(r) {
			isNum = false
			break
		}
	}
	if isNum {
		return true
	}

	// Check if it's a bullet bound
	if strings.ContainsAny(token, bulletBounds) {
		return true
	}

	// Check if it's a bullet char
	lower := strings.ToLower(token)
	if strings.ContainsAny(lower, bulletChars) {
		return true
	}

	// Check if it's a Roman numeral
	if romanRe.MatchString(token) {
		return true
	}

	return false
}

// listItem handles list items
func listItem(split base.SplitLike) base.RuleAction {
	ss := split.(*SentSplit)

	if !strings.ContainsAny(ss.Split.Delimiter, bulletBounds) {
		return base.NoAction
	}

	if len(ss.Split.Buffer) > bulletSize {
		return base.NoAction
	}

	tokens := ss.BufferTokens()
	for _, token := range tokens {
		if !isBullet(token) {
			return base.NoAction
		}
	}

	return base.ActionJoin
}

// dashRight handles dashes on the right
func dashRight(split base.SplitLike) base.RuleAction {
	ss := split.(*SentSplit)
	rightToken := ss.RightToken()

	if !punct.ContainsRune(punct.Dashes, rune(rightToken[0])) {
		return base.NoAction
	}

	right := ss.RightWord()
	if right != "" && isLowerAlpha(right) {
		return base.ActionJoin
	}

	return base.NoAction
}

// SentSegmenter segments sentences
type SentSegmenter struct {
	*base.Segmenter
}

// NewSentSegmenter creates a new SentSegmenter
func NewSentSegmenter() *SentSegmenter {
	splitter := NewSentSplitter()
	rules := []base.Rule{
		base.NewFunctionRule("empty_side", emptySide),
		base.NewFunctionRule("no_space_prefix", noSpacePrefix),
		base.NewFunctionRule("lower_right", lowerRight),
		base.NewFunctionRule("delimiter_right", delimiterRight),
		base.NewFunctionRule("sokr_left", sokrLeft),
		base.NewFunctionRule("inside_pair_sokr", insidePairSokr),
		base.NewFunctionRule("initials_left", initialsLeft),
		base.NewFunctionRule("list_item", listItem),
		base.NewFunctionRule("close_quote", closeQuote),
		base.NewFunctionRule("close_bracket", closeBracket),
		base.NewFunctionRule("dash_right", dashRight),
	}

	return &SentSegmenter{
		Segmenter: base.NewSegmenter(splitter, rules),
	}
}

// Segment overrides base segment for sentence-specific behavior
func (ss *SentSegmenter) Segment(parts []interface{}) []string {
	if len(parts) == 0 {
		return nil
	}

	var result []string
	buffer := ""

	// Get first element
	if str, ok := parts[0].(string); ok {
		buffer = str
	} else {
		return nil
	}

	i := 1
	for i < len(parts) {
		split, ok := parts[i].(*SentSplit)
		if !ok {
			i++
			continue
		}

		i++
		if i >= len(parts) {
			break
		}

		right, ok := parts[i].(string)
		if !ok {
			break
		}

		split.Split.Buffer = buffer
		if ss.Segmenter.Join(split.Split) {
			buffer = buffer + split.GetBaseSplit().Delimiter + right
		} else {
			result = append(result, buffer+split.GetBaseSplit().Delimiter)
			buffer = right
		}

		i++
	}

	if buffer != "" {
		result = append(result, buffer)
	}

	return result
}

// Post processes segments (trim whitespace for sentences)
func (ss *SentSegmenter) Post(chunks []string) []string {
	result := make([]string, 0, len(chunks))
	for _, chunk := range chunks {
		trimmed := strings.TrimSpace(chunk)
		if trimmed != "" {
			result = append(result, trimmed)
		}
	}
	return result
}
