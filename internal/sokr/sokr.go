package sokr

// makeSokrSet creates a set from space-separated words
func makeSokrSet(lines ...string) map[string]bool {
	set := make(map[string]bool)
	for _, line := range lines {
		words := splitWords(line)
		for _, word := range words {
			set[word] = true
		}
	}
	return set
}

// splitWords splits a string by whitespace
func splitWords(s string) []string {
	var words []string
	current := ""
	for _, r := range s {
		if r == ' ' || r == '\t' || r == '\n' {
			if current != "" {
				words = append(words, current)
				current = ""
			}
		} else {
			current += string(r)
		}
	}
	if current != "" {
		words = append(words, current)
	}
	return words
}

// makePairSokrSet creates a set of pairs
func makePairSokrSet(lines ...string) map[[2]string]bool {
	set := make(map[[2]string]bool)
	for _, line := range lines {
		words := splitWords(line)
		if len(words) == 2 {
			set[[2]string{words[0], words[1]}] = true
		}
	}
	return set
}

var (
	// TailSokrs are abbreviations that appear after numbers/words
	TailSokrs = makeSokrSet(
		"дес тыс млн млрд",
		"дол долл",
		"коп руб р",
		"проц",
		"га",
		"барр",
		"куб",
		"кв км",
		"см",
		"час мин сек",
		"в вв",
		"г гг",
		"с стр",
		"co corp inc",
		"изд ed",
		"др",
		"al",
	)

	// HeadSokrs are abbreviations that appear before words
	HeadSokrs = makeSokrSet(
		"букв",
		"ст",
		"трад",
		"лат венг исп кат укр нем англ фр итал греч",
		"евр араб яп слав кит рус русск латв",
		"словацк хорв",
		"mr mrs ms dr vs",
		"св",
		"арх зав зам проф акад",
		"кн",
		"корр",
		"ред",
		"гр",
		"ср",
		"чл корр",
		"им",
		"тов",
		"нач пол",
		"chap",
		"п пп ст ч чч гл стр абз пт",
		"no",
		"просп пр ул ш г гор д стр к корп пер корп обл эт пом ауд оф ком комн каб",
		"домовлад лит",
		"т",
		"рп пос с х",
		"пл",
		"bd",
		"о оз",
		"р",
		"а",
		"обр",
		"ум",
		"ок",
		"откр",
		"пс ps",
		"upd",
		"см",
		"напр",
		"доп",
		"юр физ",
		"тел",
		"сб",
		"внутр",
		"дифф",
		"гос",
		"отм",
	)

	// OtherSokrs are other abbreviations
	OtherSokrs = makeSokrSet(
		"сокр рис искл прим",
		"яз",
		"устар",
		"шутл",
	)

	// TailPairSokrs are paired abbreviations that appear after
	TailPairSokrs = makePairSokrSet(
		"т п",
		"т д",
		"у е",
		"н э",
		"p m",
		"a m",
		"с г",
		"р х",
		"с г",
		"с ш",
		"з д",
		"л с",
		"ч т", "т д",
	)

	// HeadPairSokrs are paired abbreviations that appear before
	HeadPairSokrs = makePairSokrSet(
		"т е",
		"т к",
		"т н",
		"и о",
		"к н",
		"к п", "п н",
		"к т", "т н",
		"л д",
	)

	// OtherPairSokrs are other paired abbreviations
	OtherPairSokrs = makePairSokrSet(
		"ед ч",
		"мн ч",
		"повел накл",
		"жен р",
		"муж р",
	)

	// Initials are special initial abbreviations
	Initials = map[string]bool{
		"дж": true,
		"ed": true,
		"вс": true,
	}
)

// Sokrs combines all abbreviations
var Sokrs map[string]bool

// PairSokrs combines all paired abbreviations
var PairSokrs map[[2]string]bool

func init() {
	// Combine all sokrs
	Sokrs = make(map[string]bool)
	for k := range TailSokrs {
		Sokrs[k] = true
	}
	for k := range HeadSokrs {
		Sokrs[k] = true
	}
	for k := range OtherSokrs {
		Sokrs[k] = true
	}

	// Combine all pair sokrs
	PairSokrs = make(map[[2]string]bool)
	for k := range TailPairSokrs {
		PairSokrs[k] = true
	}
	for k := range HeadPairSokrs {
		PairSokrs[k] = true
	}
	for k := range OtherPairSokrs {
		PairSokrs[k] = true
	}
}
