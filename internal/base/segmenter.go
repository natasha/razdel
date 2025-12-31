package base

import (
	"strings"
)

// Segmenter is the base type for segmenters
type Segmenter struct {
	Splitter Splitter
	Rules    []Rule
}

// NewSegmenter creates a new Segmenter
func NewSegmenter(splitter Splitter, rules []Rule) *Segmenter {
	return &Segmenter{
		Splitter: splitter,
		Rules:    rules,
	}
}

// Join determines whether to join at this split point
func (s *Segmenter) Join(split SplitLike) bool {
	for _, rule := range s.Rules {
		action := rule.Apply(split)
		if action != NoAction {
			return action == ActionJoin
		}
	}
	return false
}

// Segment processes parts and returns segments
func (s *Segmenter) Segment(parts []interface{}) []string {
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
		// parts should alternate: SplitLike, string, SplitLike, string, ...
		split, ok := parts[i].(SplitLike)
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

		baseSplit := split.GetBaseSplit()
		baseSplit.Buffer = buffer
		if baseSplit.Delimiter == "" && s.Join(split) {
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

// Post processes segments (can be overridden)
func (s *Segmenter) Post(chunks []string) []string {
	// Default: trim whitespace
	result := make([]string, 0, len(chunks))
	for _, chunk := range chunks {
		trimmed := strings.TrimSpace(chunk)
		if trimmed != "" {
			result = append(result, trimmed)
		}
	}
	return result
}
