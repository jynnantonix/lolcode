This test checks that the equality operator works correctly with floating point decimal typed arguments.  Note that boolean values can not be cast to strings so this test first implicitly casts the resulting boolean values to integer values and prints these out instead.

HAI
	I HAS A var1 ITZ 0.0
	I HAS A var2 ITZ 1.234
	VISIBLE SUM OF 0 AN BOTH SAEM var1 AN var2 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM var1 AN FAIL MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM FAIL AN var2 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM var1 AN WIN MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM WIN AN var2 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM var1 AN 0 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM 0 AN var2 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM var1 AN 1 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM 1 AN var2 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM var1 AN 0.0 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM 0.0 AN var2 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM var1 AN 1.234 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM 1.234 AN var2 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM var1 AN "0" MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM "0" AN var2 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM var1 AN "1" MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM "1" AN var2 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM var1 AN "0.0" MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM "0.0" AN var2 MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM var1 AN "1.234" MKAY?
	VISIBLE SUM OF 0 AN BOTH SAEM "1.234" AN var2 MKAY?
KTHXBAI
