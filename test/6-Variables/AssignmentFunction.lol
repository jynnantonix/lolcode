OBTW Since TEST is not declared in this function, if it has been declared in one of the parents of this function, then that variable's value will be changed. In other words, this shows how functions have access to global variables. This has been purposefully left in to give the programmer more power when it comes to manipulating variables. However if in doubt, the programmer should always declare variable before using them. TLDR

HAI,	BTW testing assignment statements

HOW DUZ I testAssign YR value
    TEST R value
    FOUND YR TEST
IF U SAY SO

HOW DUZ I testDecl YR value
    I HAS A TEST ITZ value
    FOUND YR TEST
IF U SAY SO

I HAS A TEST ITZ 3
VISIBLE "test is" TEST MKAY?, 			BTW TEST should be 3
VISIBLE "test is" testDecl 4 MKAY? MKAY?, 	BTW TEST should be 4
VISIBLE "test is" TEST MKAY?, 			BTW TEST should be 3
VISIBLE "test is" testAssign 5 MKAY? MKAY?, 	BTW TEST should be 5
VISIBLE "test is" TEST MKAY?, 			BTW TEST should be 5

KTHXBAI


