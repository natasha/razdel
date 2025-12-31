package base

// Split represents a potential split point in text
type Split struct {
	Left      string
	Delimiter string
	Right     string
	Buffer    string
}

// NewSplit creates a new Split
func NewSplit(left, delimiter, right string) *Split {
	return &Split{
		Left:      left,
		Delimiter: delimiter,
		Right:     right,
	}
}

// SplitLike is an interface for split-like objects
type SplitLike interface {
	GetBaseSplit() *Split
}

// GetBaseSplit returns the split itself (implements SplitLike)
func (s *Split) GetBaseSplit() *Split {
	return s
}

// Splitter is an interface for objects that can split text into parts
type Splitter interface {
	Split(text string) []interface{}
}
