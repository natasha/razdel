package razdel

import "fmt"

// Substring represents a substring with its position in the original text
type Substring struct {
	Start int
	Stop  int
	Text  string
}

// String returns a string representation of the substring
func (s Substring) String() string {
	return fmt.Sprintf("Substring(%d, %d, %q)", s.Start, s.Stop, s.Text)
}

// findSubstrings converts chunks to Substring objects by finding their positions in text
func findSubstrings(chunks []string, text string) []Substring {
	result := make([]Substring, 0, len(chunks))
	offset := 0

	for _, chunk := range chunks {
		if chunk == "" {
			continue
		}
		start := offset
		for start < len(text) && text[start:start+len(chunk)] != chunk {
			start++
		}
		if start >= len(text) {
			// Not found, shouldn't happen
			continue
		}
		stop := start + len(chunk)
		result = append(result, Substring{
			Start: start,
			Stop:  stop,
			Text:  chunk,
		})
		offset = stop
	}

	return result
}
