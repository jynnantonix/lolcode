This test checks that a function with a nil return value works correctly.  Note that nil values cannot be implicitly cast to string values directly and thus this test first implicitly casts them to boolean values which are then cast to integer values which are then cast to string values.

HAI 1.2
	HOW DUZ I fun1
		"a"
		FOUND YR NOOB
	IF U SAY SO

	HOW DUZ I fun2 YR arg
		arg
		FOUND YR NOOB
	IF U SAY SO

	VISIBLE SUM OF 0 AN NOT fun1 MKAY? MKAY?
	VISIBLE SUM OF 0 AN NOT fun2 "b" MKAY? MKAY?
KTHXBAI
