package tokenize

import (
	"regexp"
	"strings"
	"unicode"

	"github.com/natasha/razdel/internal/base"
	"github.com/natasha/razdel/internal/punct"
)

// AtomType represents the type of an atom
type AtomType string

const (
	RU    AtomType = "RU"
	LAT   AtomType = "LAT"
	INT   AtomType = "INT"
	PUNCT AtomType = "PUNCT"
	OTHER AtomType = "OTHER"
)

// Atom represents a basic unit of text
type Atom struct {
	Start  int
	Stop   int
	Type   AtomType
	Text   string
	Normal string
}

// Puncts is the set of punctuation characters
const Puncts = "\\/!#$%&*+,.:;<=>?@^_`|~№…" + punct.Dashes + punct.Quotes + punct.Brackets

// buildAtomRegex builds the atom regex pattern
func buildAtomRegex() *regexp.Regexp {
	// Manually escape special characters for character class
	// In character class, we need to escape: ] \ ^ -
	escaped := ""
	for _, r := range Puncts {
		s := string(r)
		if s == "\\" || s == "]" || s == "^" || s == "-" {
			escaped += "\\" + s
		} else {
			escaped += s
		}
	}
	pattern := `(?i)([а-яё]+)|([a-z]+)|(\d+)|([` + escaped + `])|(\S)`
	return regexp.MustCompile(pattern)
}

// atomRegex matches atoms in text
var atomRegex = buildAtomRegex()

// smileRegex matches smiles
var smileRegex = regexp.MustCompile(`^` + punct.SmilesPattern + `$`)

// TokenSplit represents a split point for tokenization
type TokenSplit struct {
	*base.Split
	LeftAtoms  []*Atom
	RightAtoms []*Atom
}

// Left1 returns the last atom on the left
func (ts *TokenSplit) Left1() *Atom {
	if len(ts.LeftAtoms) > 0 {
		return ts.LeftAtoms[len(ts.LeftAtoms)-1]
	}
	return nil
}

// Left2 returns the second to last atom on the left
func (ts *TokenSplit) Left2() *Atom {
	if len(ts.LeftAtoms) > 1 {
		return ts.LeftAtoms[len(ts.LeftAtoms)-2]
	}
	return nil
}

// Right1 returns the first atom on the right
func (ts *TokenSplit) Right1() *Atom {
	if len(ts.RightAtoms) > 0 {
		return ts.RightAtoms[0]
	}
	return nil
}

// Right2 returns the second atom on the right
func (ts *TokenSplit) Right2() *Atom {
	if len(ts.RightAtoms) > 1 {
		return ts.RightAtoms[1]
	}
	return nil
}

// TokenSplitter splits text into atoms
type TokenSplitter struct {
	Window int
}

// NewTokenSplitter creates a new TokenSplitter
func NewTokenSplitter() *TokenSplitter {
	return &TokenSplitter{Window: 3}
}

// extractAtoms extracts atoms from text
func (ts *TokenSplitter) extractAtoms(text string) []*Atom {
	matches := atomRegex.FindAllStringSubmatchIndex(text, -1)
	atoms := make([]*Atom, 0, len(matches))

	for _, match := range matches {
		start := match[0]
		stop := match[1]
		atomText := text[start:stop]

		var atomType AtomType
		// Determine type based on which group matched
		if match[2] != -1 { // RU
			atomType = RU
		} else if match[4] != -1 { // LAT
			atomType = LAT
		} else if match[6] != -1 { // INT
			atomType = INT
		} else if match[8] != -1 { // PUNCT
			atomType = PUNCT
		} else { // OTHER
			atomType = OTHER
		}

		atoms = append(atoms, &Atom{
			Start:  start,
			Stop:   stop,
			Type:   atomType,
			Text:   atomText,
			Normal: strings.ToLower(atomText),
		})
	}

	return atoms
}

// Split implements the Splitter interface
func (ts *TokenSplitter) Split(text string) []interface{} {
	atoms := ts.extractAtoms(text)
	var result []interface{}

	for i, atom := range atoms {
		if i > 0 {
			prev := atoms[i-1]
			delimiter := text[prev.Stop:atom.Start]

			leftStart := maxInt(0, i-ts.Window)
			left := atoms[leftStart:i]
			rightEnd := minInt(len(atoms), i+ts.Window)
			right := atoms[i:rightEnd]

			split := &TokenSplit{
				Split: base.NewSplit(
					prev.Text,
					delimiter,
					atom.Text,
				),
				LeftAtoms:  left,
				RightAtoms: right,
			}
			result = append(result, split)
		}
		result = append(result, atom.Text)
	}

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

// Rules for tokenization

// splitSpace splits on whitespace
func splitSpace(split base.SplitLike) base.RuleAction {
	if split.GetBaseSplit().Delimiter != "" {
		return base.ActionSplit
	}
	return base.NoAction
}

// DashRule joins tokens separated by dashes
type DashRule struct{}

func (r *DashRule) Name() string { return "dash" }

func (r *DashRule) Apply(split base.SplitLike) base.RuleAction {
	ts, ok := split.(*TokenSplit)
	if !ok {
		return base.NoAction
	}

	var left, right *Atom
	delim := ts.Split.Delimiter
	if len(delim) == 0 {
		return base.NoAction
	}
	if punct.ContainsRune(punct.Dashes, rune(delim[0])) && len(delim) == 1 {
		left = ts.Left1()
		right = ts.Right1()
	} else {
		return base.NoAction
	}

	if left == nil || right == nil {
		return base.NoAction
	}

	if left.Type == PUNCT || right.Type == PUNCT {
		return base.NoAction
	}

	return base.ActionJoin
}

// UnderscoreRule joins tokens separated by underscores
type UnderscoreRule struct{}

func (r *UnderscoreRule) Name() string { return "underscore" }

func (r *UnderscoreRule) Apply(split base.SplitLike) base.RuleAction {
	ts, ok := split.(*TokenSplit)
	if !ok {
		return base.NoAction
	}

	if ts.Split.Delimiter != "_" {
		return base.NoAction
	}

	left := ts.Left1()
	right := ts.Right1()

	if left == nil || right == nil {
		return base.NoAction
	}

	if left.Type == PUNCT || right.Type == PUNCT {
		return base.NoAction
	}

	return base.ActionJoin
}

// FloatRule joins numbers separated by . or ,
type FloatRule struct{}

func (r *FloatRule) Name() string { return "float" }

func (r *FloatRule) Apply(split base.SplitLike) base.RuleAction {
	ts, ok := split.(*TokenSplit)
	if !ok {
		return base.NoAction
	}

	if ts.Split.Delimiter != "." && ts.Split.Delimiter != "," {
		return base.NoAction
	}

	left := ts.Left1()
	right := ts.Right1()

	if left == nil || right == nil {
		return base.NoAction
	}

	if left.Type == INT && right.Type == INT {
		return base.ActionJoin
	}

	return base.NoAction
}

// FractionRule joins numbers separated by / or \
type FractionRule struct{}

func (r *FractionRule) Name() string { return "fraction" }

func (r *FractionRule) Apply(split base.SplitLike) base.RuleAction {
	ts, ok := split.(*TokenSplit)
	if !ok {
		return base.NoAction
	}

	if ts.Split.Delimiter != "/" && ts.Split.Delimiter != "\\" {
		return base.NoAction
	}

	left := ts.Left1()
	right := ts.Right1()

	if left == nil || right == nil {
		return base.NoAction
	}

	if left.Type == INT && right.Type == INT {
		return base.ActionJoin
	}

	return base.NoAction
}

// punctRule joins consecutive punctuation
func punctRule(split base.SplitLike) base.RuleAction {
	ts, ok := split.(*TokenSplit)
	if !ok {
		return base.NoAction
	}

	left := ts.Left1()
	right := ts.Right1()

	if left == nil || right == nil {
		return base.NoAction
	}

	if left.Type != PUNCT || right.Type != PUNCT {
		return base.NoAction
	}

	// Check for smiles
	if smileRegex.MatchString(ts.Split.Buffer + ts.Split.Right) {
		return base.ActionJoin
	}

	// Join endings like ... ?!
	if punct.ContainsRune(punct.Endings, rune(ts.Split.Left[0])) &&
		punct.ContainsRune(punct.Endings, rune(ts.Split.Right[0])) {
		return base.ActionJoin
	}

	// Join -- or **
	if ts.Split.Left+ts.Split.Right == "--" || ts.Split.Left+ts.Split.Right == "**" {
		return base.ActionJoin
	}

	return base.NoAction
}

// otherRule joins OTHER type atoms with letters
func otherRule(split base.SplitLike) base.RuleAction {
	ts, ok := split.(*TokenSplit)
	if !ok {
		return base.NoAction
	}

	left := ts.Left1()
	right := ts.Right1()

	if left == nil || right == nil {
		return base.NoAction
	}

	if left.Type == OTHER && (right.Type == OTHER || right.Type == RU || right.Type == LAT) {
		return base.ActionJoin
	}

	if (left.Type == OTHER || left.Type == RU || left.Type == LAT) && right.Type == OTHER {
		return base.ActionJoin
	}

	return base.NoAction
}

// yahooRule handles special case for yahoo!
func yahooRule(split base.SplitLike) base.RuleAction {
	ts, ok := split.(*TokenSplit)
	if !ok {
		return base.NoAction
	}

	left := ts.Left1()
	if left != nil && left.Normal == "yahoo" && ts.Split.Right == "!" {
		return base.ActionJoin
	}

	return base.NoAction
}

// TokenSegmenter segments tokens
type TokenSegmenter struct {
	*base.Segmenter
}

// NewTokenSegmenter creates a new TokenSegmenter
func NewTokenSegmenter() *TokenSegmenter {
	splitter := NewTokenSplitter()
	rules := []base.Rule{
		&DashRule{},
		&UnderscoreRule{},
		&FloatRule{},
		&FractionRule{},
		base.NewFunctionRule("punct", punctRule),
		base.NewFunctionRule("other", otherRule),
		base.NewFunctionRule("yahoo", yahooRule),
	}

	return &TokenSegmenter{
		Segmenter: base.NewSegmenter(splitter, rules),
	}
}

// Segment overrides base segment for token-specific behavior
func (ts *TokenSegmenter) Segment(parts []interface{}) []string {
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
		// parts should alternate: Split, string, Split, string, ...
		split, ok := parts[i].(*TokenSplit)
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
		// For tokens, we don't join if there's a delimiter, unless the rule says so
		if split.GetBaseSplit().Delimiter == "" && ts.Segmenter.Join(split) {
			buffer += right
		} else {
			result = append(result, buffer)
			buffer = right
		}

		i++
	}

	if buffer != "" {
		result = append(result, buffer)
	}

	return result
}

// Post processes segments (no trimming for tokens)
func (ts *TokenSegmenter) Post(chunks []string) []string {
	return chunks
}

// isLowerAlpha checks if a string is all lowercase letters
func isLowerAlpha(s string) bool {
	if s == "" {
		return false
	}
	for _, r := range s {
		if !unicode.IsLetter(r) || !unicode.IsLower(r) {
			return false
		}
	}
	return true
}
