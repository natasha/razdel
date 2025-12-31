package punct

// Punctuation constants
const (
	Endings = ".?!…"
	Dashes  = "‑–—−-"

	OpenQuotes    = `«"'`
	CloseQuotes   = `»"'`
	GenericQuotes = `"„'`
	Quotes        = OpenQuotes + CloseQuotes + GenericQuotes

	OpenBrackets  = "([{"
	CloseBrackets = ")]}"
	Brackets      = OpenBrackets + CloseBrackets

	Bounds = Quotes + Brackets

	// Smiles regex pattern: [=:;]-?[)(]{1,3}
	SmilesPattern = `[=:;]-?[)(]{1,3}`
)

// ContainsRune checks if a string contains a rune
func ContainsRune(s string, r rune) bool {
	for _, c := range s {
		if c == r {
			return true
		}
	}
	return false
}

// ContainsAny checks if s contains any rune from chars
func ContainsAny(s, chars string) bool {
	for _, r := range s {
		if ContainsRune(chars, r) {
			return true
		}
	}
	return false
}
