This test checks that whitespace in between tokens is handled properly.  It
tests whitespace only, tabs only, alternating whitespace and tabs, and
alternating tabs and whitespace.
HAI
	VISIBLE    "Lorem "    "ipsum "    "dolor "    "sit" MKAY?
	VISIBLE			"Lorem "			"ipsum "			"dolor "			"sit" MKAY?
	VISIBLE 	 "Lorem " 	 "ipsum " 	 "dolor " 	 "sit" MKAY?
	VISIBLE	 	"Lorem "	 	"ipsum "	 	"dolor "	 	"sit" MKAY?
KTHXBAI

