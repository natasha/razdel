// Package razdel provides rule-based Russian sentence and word tokenization.
//
// Example usage for tokenization:
//
//	tokens := razdel.Tokenize("Кружка-термос на 0.5л (50/64 см³, 516;...)")
//	for _, token := range tokens {
//	    fmt.Printf("%s\n", token.Text)
//	}
//
// Example usage for sentence segmentation:
//
//	sents := razdel.Sentenize(`- "Так в чем же дело?" - "Не ра-ду-ют". И т. д. и т. п. В общем, вся газета`)
//	for _, sent := range sents {
//	    fmt.Printf("%s\n", sent.Text)
//	}
package razdel

import (
	"github.com/natasha/razdel/internal/sentenize"
	"github.com/natasha/razdel/internal/tokenize"
)

var (
	tokenSegmenter = tokenize.NewTokenSegmenter()
	sentSegmenter  = sentenize.NewSentSegmenter()
)

// Tokenize splits text into tokens and returns a slice of Substring objects.
// Each Substring contains the start and stop positions of the token in the original text.
//
// Example:
//
//	tokens := razdel.Tokenize("Кружка-термос на 0.5л")
//	// Returns:
//	// [Substring(0, 13, "Кружка-термос"), Substring(14, 16, "на"), Substring(17, 20, "0.5"), Substring(20, 21, "л")]
func Tokenize(text string) []Substring {
	parts := tokenSegmenter.Segmenter.Splitter.Split(text)
	chunks := tokenSegmenter.Segment(parts)
	chunks = tokenSegmenter.Post(chunks)
	return findSubstrings(chunks, text)
}

// Sentenize splits text into sentences and returns a slice of Substring objects.
// Each Substring contains the start and stop positions of the sentence in the original text.
//
// Example:
//
//	sents := razdel.Sentenize(`- "Так в чем же дело?" - "Не ра-ду-ют". И т. д. и т. п.`)
//	// Returns:
//	// [Substring(0, 22, "- \"Так в чем же дело?\""), Substring(23, 39, "- \"Не ра-ду-ют\"."), Substring(40, 55, "И т. д. и т. п.")]
func Sentenize(text string) []Substring {
	parts := sentSegmenter.Segmenter.Splitter.Split(text)
	chunks := sentSegmenter.Segment(parts)
	chunks = sentSegmenter.Post(chunks)
	return findSubstrings(chunks, text)
}
