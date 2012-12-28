Recursively calculates the given base to the given power.
HAI,	BTW power function

HOW DUZ I pow YR base AN YR exp
	BTW Base Cases
	BOTH SAEM exp AN 0, O RLY?
		YA RLY, FOUND YR 1
	OIC	

	BOTH SAEM exp AN 1, O RLY?
		YA RLY, FOUND YR base
	OIC

	BTW Recursive case
	I HAS A num
	I HAS A newExp

	QUOSHUNT OF exp AN 2,		BTW IT = exp / 2
	newExp R MAEK IT A NUMBR,	BTW newExp = floor(IT)

	OBTW Checking to see if the exponent is odd.
	If it is then we set IT = base, otherwise IT = 1 TLDR
	DIFFRINT 0 AN MOD OF exp AN 2, O RLY?
		YA RLY, IT R base
		NO WAI, IT R 1
	OIC

	num R pow base newExp MKAY?,	BTW num = pow(base exp)
	num R PRODUKT OF num AN num,	BTW num = num * num

	FOUND YR PRODUKT OF IT AN num,	BTW return IT * num
IF U SAY SO

I HAS A base
I HAS A exp

VISIBLE "What is the base?" MKAY?
GIMMEH base

BTW base R MAEK base A NUMBR

VISIBLE "What is the exponent?" MKAY?
GIMMEH exp

BTW exp R MAEK exp A NUMBR

VISIBLE base "to the" exp "is" pow base exp MKAY? MKAY?

KTHXBAI


	