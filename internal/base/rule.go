package base

// RuleAction represents the action a rule can return
type RuleAction string

const (
	// ActionSplit indicates that the split point should be kept
	ActionSplit RuleAction = "split"
	// ActionJoin indicates that the split point should be joined
	ActionJoin RuleAction = "join"
	// NoAction indicates no action (continue to next rule)
	NoAction RuleAction = ""
)

// Rule represents a rule that determines whether to join or split at a given split point
type Rule interface {
	Apply(split SplitLike) RuleAction
	Name() string
}

// FunctionRule wraps a function as a Rule
type FunctionRule struct {
	name string
	fn   func(SplitLike) RuleAction
}

// NewFunctionRule creates a new FunctionRule
func NewFunctionRule(name string, fn func(SplitLike) RuleAction) *FunctionRule {
	return &FunctionRule{name: name, fn: fn}
}

// Apply applies the function rule
func (r *FunctionRule) Apply(split SplitLike) RuleAction {
	return r.fn(split)
}

// Name returns the rule name
func (r *FunctionRule) Name() string {
	return r.name
}
