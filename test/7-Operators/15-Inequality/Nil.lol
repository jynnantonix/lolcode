This test checks that the inequality operator works correctly with nil typed arguments.  Note that boolean values can not be cast to strings so this test first implicitly casts the resulting boolean values to integer values and prints these out instead.

HAI
	I HAS A var1
	I HAS A var2
	VISIBLE SUM OF 0 AN DIFFRINT var1 AN var2 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT var1 AN FAIL MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT FAIL AN var2 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT var1 AN WIN MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT WIN AN var2 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT var1 AN 0 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT 0 AN var2 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT var1 AN 1 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT 1 AN var2 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT var1 AN 0.0 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT 0.0 AN var2 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT var1 AN 1.234 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT 1.234 AN var2 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT var1 AN "0" MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT "0" AN var2 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT var1 AN "1" MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT "1" AN var2 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT var1 AN "0.0" MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT "0.0" AN var2 MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT var1 AN "1.234" MKAY?
	VISIBLE SUM OF 0 AN DIFFRINT "1.234" AN var2 MKAY?
KTHXBAI
