<html>
<head>
<title>scheme_tokens.py</title>
<link href="css/assignments.css" rel="stylesheet" type="text/css">
</head>

<body>
<h3>scheme_tokens.py (<a href="scheme_tokens.py">plain text</a>)</h3>
<hr>
<pre>
<span style="color: darkred">"""The scheme_tokens module provides functions tokenize_line and tokenize_lines
for converting (iterators producing) strings into (iterators producing) lists
of tokens.  A token may be:

  * A number (represented as an int or float)
  * A boolean (represented as a bool)
  * A symbol (represented as a string)
  * A delimiter, including parentheses, dots, and single quotes

This file also includes some features of Scheme that have not been addressed
in the course, such as quasiquoting and Scheme strings.
"""

</span><span style="color: blue; font-weight: bold">from </span>ucb <span style="color: blue; font-weight: bold">import </span>main
<span style="color: blue; font-weight: bold">import </span>itertools
<span style="color: blue; font-weight: bold">import </span>string
<span style="color: blue; font-weight: bold">import </span>sys
<span style="color: blue; font-weight: bold">import </span>tokenize

_NUMERAL_STARTS <span style="font-weight: bold">= </span>set<span style="font-weight: bold">(</span>string<span style="font-weight: bold">.</span>digits<span style="font-weight: bold">) | </span>set<span style="font-weight: bold">(</span><span style="color: red">'+-.'</span><span style="font-weight: bold">)
</span>_SYMBOL_CHARS <span style="font-weight: bold">= (</span>set<span style="font-weight: bold">(</span><span style="color: red">'!$%&amp;*/:&lt;=&gt;?@^_~'</span><span style="font-weight: bold">) | </span>set<span style="font-weight: bold">(</span>string<span style="font-weight: bold">.</span>ascii_lowercase<span style="font-weight: bold">) |
                 </span>set<span style="font-weight: bold">(</span>string<span style="font-weight: bold">.</span>ascii_uppercase<span style="font-weight: bold">) | </span>_NUMERAL_STARTS<span style="font-weight: bold">)
</span>_STRING_DELIMS <span style="font-weight: bold">= </span>set<span style="font-weight: bold">(</span><span style="color: red">'"'</span><span style="font-weight: bold">)
</span>_WHITESPACE <span style="font-weight: bold">= </span>set<span style="font-weight: bold">(</span><span style="color: red">' \t\n\r'</span><span style="font-weight: bold">)
</span>_SINGLE_CHAR_TOKENS <span style="font-weight: bold">= </span>set<span style="font-weight: bold">(</span><span style="color: red">"()'`"</span><span style="font-weight: bold">)
</span>_TOKEN_END <span style="font-weight: bold">= </span>_WHITESPACE <span style="font-weight: bold">| </span>_SINGLE_CHAR_TOKENS <span style="font-weight: bold">| </span>_STRING_DELIMS <span style="font-weight: bold">| {</span><span style="color: red">','</span><span style="font-weight: bold">, </span><span style="color: red">',@'</span><span style="font-weight: bold">}
</span>DELIMITERS <span style="font-weight: bold">= </span>_SINGLE_CHAR_TOKENS <span style="font-weight: bold">| {</span><span style="color: red">'.'</span><span style="font-weight: bold">, </span><span style="color: red">','</span><span style="font-weight: bold">, </span><span style="color: red">',@'</span><span style="font-weight: bold">}

</span><span style="color: blue; font-weight: bold">def </span>valid_symbol<span style="font-weight: bold">(</span>s<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Returns whether s is not a well-formed value."""
    </span><span style="color: blue; font-weight: bold">if </span>len<span style="font-weight: bold">(</span>s<span style="font-weight: bold">) == </span><span style="color: red">0</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return False
    for </span>c <span style="color: blue; font-weight: bold">in </span>s<span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">if </span>c <span style="color: blue; font-weight: bold">not in </span>_SYMBOL_CHARS<span style="font-weight: bold">:
            </span><span style="color: blue; font-weight: bold">return False
    return True

def </span>next_candidate_token<span style="font-weight: bold">(</span>line<span style="font-weight: bold">, </span>k<span style="font-weight: bold">):
    </span><span style="color: darkred">"""A tuple (tok, k'), where tok is the next substring of line at or
    after position k that could be a token (assuming it passes a validity
    check), and k' is the position in line following that token.  Returns
    (None, len(line)) when there are no more tokens."""
    </span><span style="color: blue; font-weight: bold">while </span>k <span style="font-weight: bold">&lt; </span>len<span style="font-weight: bold">(</span>line<span style="font-weight: bold">):
        </span>c <span style="font-weight: bold">= </span>line<span style="font-weight: bold">[</span>k<span style="font-weight: bold">]
        </span><span style="color: blue; font-weight: bold">if </span>c <span style="font-weight: bold">== </span><span style="color: red">';'</span><span style="font-weight: bold">:
            </span><span style="color: blue; font-weight: bold">return </span><span style="color: blue">None</span><span style="font-weight: bold">, </span>len<span style="font-weight: bold">(</span>line<span style="font-weight: bold">)
        </span><span style="color: blue; font-weight: bold">elif </span>c <span style="color: blue; font-weight: bold">in </span>_WHITESPACE<span style="font-weight: bold">:
            </span>k <span style="font-weight: bold">+= </span><span style="color: red">1
        </span><span style="color: blue; font-weight: bold">elif </span>c <span style="color: blue; font-weight: bold">in </span>_SINGLE_CHAR_TOKENS<span style="font-weight: bold">:
            </span><span style="color: blue; font-weight: bold">return </span>c<span style="font-weight: bold">, </span>k<span style="font-weight: bold">+</span><span style="color: red">1
        </span><span style="color: blue; font-weight: bold">elif </span>c <span style="font-weight: bold">== </span><span style="color: red">'#'</span><span style="font-weight: bold">:  </span><span style="color: green; font-style: italic"># Boolean values #t and #f
            </span><span style="color: blue; font-weight: bold">return </span>line<span style="font-weight: bold">[</span>k<span style="font-weight: bold">:</span>k<span style="font-weight: bold">+</span><span style="color: red">2</span><span style="font-weight: bold">], </span>min<span style="font-weight: bold">(</span>k<span style="font-weight: bold">+</span><span style="color: red">2</span><span style="font-weight: bold">, </span>len<span style="font-weight: bold">(</span>line<span style="font-weight: bold">))
        </span><span style="color: blue; font-weight: bold">elif </span>c <span style="font-weight: bold">== </span><span style="color: red">','</span><span style="font-weight: bold">: </span><span style="color: green; font-style: italic"># Unquote; check for @
            </span><span style="color: blue; font-weight: bold">if </span>k<span style="font-weight: bold">+</span><span style="color: red">1 </span><span style="font-weight: bold">&lt; </span>len<span style="font-weight: bold">(</span>line<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">and </span>line<span style="font-weight: bold">[</span>k<span style="font-weight: bold">+</span><span style="color: red">1</span><span style="font-weight: bold">] == </span><span style="color: red">'@'</span><span style="font-weight: bold">:
                </span><span style="color: blue; font-weight: bold">return </span><span style="color: red">',@'</span><span style="font-weight: bold">, </span>k<span style="font-weight: bold">+</span><span style="color: red">2
            </span><span style="color: blue; font-weight: bold">return </span>c<span style="font-weight: bold">, </span>k<span style="font-weight: bold">+</span><span style="color: red">1
        </span><span style="color: blue; font-weight: bold">elif </span>c <span style="color: blue; font-weight: bold">in </span>_STRING_DELIMS<span style="font-weight: bold">:
            </span><span style="color: blue; font-weight: bold">if </span>k<span style="font-weight: bold">+</span><span style="color: red">1 </span><span style="font-weight: bold">&lt; </span>len<span style="font-weight: bold">(</span>line<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">and </span>line<span style="font-weight: bold">[</span>k<span style="font-weight: bold">+</span><span style="color: red">1</span><span style="font-weight: bold">] == </span>c<span style="font-weight: bold">: </span><span style="color: green; font-style: italic"># No triple quotes in Scheme
                </span><span style="color: blue; font-weight: bold">return </span>c<span style="font-weight: bold">+</span>c<span style="font-weight: bold">, </span>k<span style="font-weight: bold">+</span><span style="color: red">2
            </span>line_bytes <span style="font-weight: bold">= (</span>bytes<span style="font-weight: bold">(</span>line<span style="font-weight: bold">[</span>k<span style="font-weight: bold">:], </span>encoding<span style="font-weight: bold">=</span><span style="color: red">'utf-8'</span><span style="font-weight: bold">),)
            </span>gen <span style="font-weight: bold">= </span>tokenize<span style="font-weight: bold">.</span>tokenize<span style="font-weight: bold">(</span>iter<span style="font-weight: bold">(</span>line_bytes<span style="font-weight: bold">).</span>__next__<span style="font-weight: bold">)
            </span>next<span style="font-weight: bold">(</span>gen<span style="font-weight: bold">) </span><span style="color: green; font-style: italic"># Throw away encoding token
            </span>token <span style="font-weight: bold">= </span>next<span style="font-weight: bold">(</span>gen<span style="font-weight: bold">)
            </span><span style="color: blue; font-weight: bold">if </span>token<span style="font-weight: bold">.</span>type <span style="font-weight: bold">!= </span>tokenize<span style="font-weight: bold">.</span>STRING<span style="font-weight: bold">:
                </span><span style="color: blue; font-weight: bold">raise </span>ValueError<span style="font-weight: bold">(</span><span style="color: red">"invalid string: {0}"</span><span style="font-weight: bold">.</span>format<span style="font-weight: bold">(</span>token<span style="font-weight: bold">.</span>string<span style="font-weight: bold">))
            </span><span style="color: blue; font-weight: bold">return </span>token<span style="font-weight: bold">.</span>string<span style="font-weight: bold">, </span>token<span style="font-weight: bold">.</span>end<span style="font-weight: bold">[</span><span style="color: red">1</span><span style="font-weight: bold">]+</span>k
        <span style="color: blue; font-weight: bold">else</span><span style="font-weight: bold">:
            </span>j <span style="font-weight: bold">= </span>k
            <span style="color: blue; font-weight: bold">while </span>j <span style="font-weight: bold">&lt; </span>len<span style="font-weight: bold">(</span>line<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">and </span>line<span style="font-weight: bold">[</span>j<span style="font-weight: bold">] </span><span style="color: blue; font-weight: bold">not in </span>_TOKEN_END<span style="font-weight: bold">:
                </span>j <span style="font-weight: bold">+= </span><span style="color: red">1
            </span><span style="color: blue; font-weight: bold">return </span>line<span style="font-weight: bold">[</span>k<span style="font-weight: bold">:</span>j<span style="font-weight: bold">], </span>min<span style="font-weight: bold">(</span>j<span style="font-weight: bold">, </span>len<span style="font-weight: bold">(</span>line<span style="font-weight: bold">))
    </span><span style="color: blue; font-weight: bold">return </span><span style="color: blue">None</span><span style="font-weight: bold">, </span>len<span style="font-weight: bold">(</span>line<span style="font-weight: bold">)

</span><span style="color: blue; font-weight: bold">def </span>tokenize_line<span style="font-weight: bold">(</span>line<span style="font-weight: bold">):
    </span><span style="color: darkred">"""The list of Scheme tokens on line.  Excludes comments and whitespace."""
    </span>result <span style="font-weight: bold">= []
    </span>text<span style="font-weight: bold">, </span>i <span style="font-weight: bold">= </span>next_candidate_token<span style="font-weight: bold">(</span>line<span style="font-weight: bold">, </span><span style="color: red">0</span><span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">while </span>text <span style="color: blue; font-weight: bold">is not </span><span style="color: blue">None</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">if </span>text <span style="color: blue; font-weight: bold">in </span>DELIMITERS<span style="font-weight: bold">:
            </span>result<span style="font-weight: bold">.</span>append<span style="font-weight: bold">(</span>text<span style="font-weight: bold">)
        </span><span style="color: blue; font-weight: bold">elif </span>text <span style="font-weight: bold">== </span><span style="color: red">'#t' </span><span style="color: blue; font-weight: bold">or </span>text<span style="font-weight: bold">.</span>lower<span style="font-weight: bold">() == </span><span style="color: red">'true'</span><span style="font-weight: bold">:
            </span>result<span style="font-weight: bold">.</span>append<span style="font-weight: bold">(</span><span style="color: blue; font-weight: bold">True</span><span style="font-weight: bold">)
        </span><span style="color: blue; font-weight: bold">elif </span>text <span style="font-weight: bold">== </span><span style="color: red">'#f' </span><span style="color: blue; font-weight: bold">or </span>text<span style="font-weight: bold">.</span>lower<span style="font-weight: bold">() == </span><span style="color: red">'false'</span><span style="font-weight: bold">:
            </span>result<span style="font-weight: bold">.</span>append<span style="font-weight: bold">(</span><span style="color: blue; font-weight: bold">False</span><span style="font-weight: bold">)
        </span><span style="color: blue; font-weight: bold">elif </span>text <span style="font-weight: bold">== </span><span style="color: red">'nil'</span><span style="font-weight: bold">:
            </span>result<span style="font-weight: bold">.</span>append<span style="font-weight: bold">(</span>text<span style="font-weight: bold">)
        </span><span style="color: blue; font-weight: bold">elif </span>text<span style="font-weight: bold">[</span><span style="color: red">0</span><span style="font-weight: bold">] </span><span style="color: blue; font-weight: bold">in </span>_SYMBOL_CHARS<span style="font-weight: bold">:
            </span>number <span style="font-weight: bold">= </span><span style="color: blue; font-weight: bold">False
            if </span>text<span style="font-weight: bold">[</span><span style="color: red">0</span><span style="font-weight: bold">] </span><span style="color: blue; font-weight: bold">in </span>_NUMERAL_STARTS<span style="font-weight: bold">:
                </span><span style="color: blue; font-weight: bold">try</span><span style="font-weight: bold">:
                    </span>result<span style="font-weight: bold">.</span>append<span style="font-weight: bold">(</span>int<span style="font-weight: bold">(</span>text<span style="font-weight: bold">))
                    </span>number <span style="font-weight: bold">= </span><span style="color: blue; font-weight: bold">True
                except </span>ValueError<span style="font-weight: bold">:
                    </span><span style="color: blue; font-weight: bold">try</span><span style="font-weight: bold">:
                        </span>result<span style="font-weight: bold">.</span>append<span style="font-weight: bold">(</span>float<span style="font-weight: bold">(</span>text<span style="font-weight: bold">))
                        </span>number <span style="font-weight: bold">= </span><span style="color: blue; font-weight: bold">True
                    except </span>ValueError<span style="font-weight: bold">:
                        </span><span style="color: blue; font-weight: bold">pass
            if not </span>number<span style="font-weight: bold">:
                </span><span style="color: blue; font-weight: bold">if </span>valid_symbol<span style="font-weight: bold">(</span>text<span style="font-weight: bold">):
                    </span>result<span style="font-weight: bold">.</span>append<span style="font-weight: bold">(</span>text<span style="font-weight: bold">.</span>lower<span style="font-weight: bold">())
                </span><span style="color: blue; font-weight: bold">else</span><span style="font-weight: bold">:
                    </span><span style="color: blue; font-weight: bold">raise </span>ValueError<span style="font-weight: bold">(</span><span style="color: red">"invalid numeral or symbol: {0}"</span><span style="font-weight: bold">.</span>format<span style="font-weight: bold">(</span>text<span style="font-weight: bold">))
        </span><span style="color: blue; font-weight: bold">elif </span>text<span style="font-weight: bold">[</span><span style="color: red">0</span><span style="font-weight: bold">] </span><span style="color: blue; font-weight: bold">in </span>_STRING_DELIMS<span style="font-weight: bold">:
            </span>result<span style="font-weight: bold">.</span>append<span style="font-weight: bold">(</span>text<span style="font-weight: bold">)
        </span><span style="color: blue; font-weight: bold">else</span><span style="font-weight: bold">:
            </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span><span style="color: red">"warning: invalid token: {0}"</span><span style="font-weight: bold">.</span>format<span style="font-weight: bold">(</span>text<span style="font-weight: bold">), </span>file<span style="font-weight: bold">=</span>sys<span style="font-weight: bold">.</span>stderr<span style="font-weight: bold">)
            </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span><span style="color: red">"    "</span><span style="font-weight: bold">, </span>line<span style="font-weight: bold">, </span>file<span style="font-weight: bold">=</span>sys<span style="font-weight: bold">.</span>stderr<span style="font-weight: bold">)
            </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span><span style="color: red">" " </span><span style="font-weight: bold">* (</span>i<span style="font-weight: bold">+</span><span style="color: red">3</span><span style="font-weight: bold">), </span><span style="color: red">"^"</span><span style="font-weight: bold">, </span>file<span style="font-weight: bold">=</span>sys<span style="font-weight: bold">.</span>stderr<span style="font-weight: bold">)
        </span>text<span style="font-weight: bold">, </span>i <span style="font-weight: bold">= </span>next_candidate_token<span style="font-weight: bold">(</span>line<span style="font-weight: bold">, </span>i<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>result

<span style="color: blue; font-weight: bold">def </span>tokenize_lines<span style="font-weight: bold">(</span>input<span style="font-weight: bold">):
    </span><span style="color: darkred">"""An iterator that returns lists of tokens, one for each line of the
    iterable input sequence."""
    </span><span style="color: blue; font-weight: bold">return </span>map<span style="font-weight: bold">(</span>tokenize_line<span style="font-weight: bold">, </span>input<span style="font-weight: bold">)

</span><span style="color: blue; font-weight: bold">def </span>count_tokens<span style="font-weight: bold">(</span>input<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Count the number of non-delimiter tokens in input."""
    </span><span style="color: blue; font-weight: bold">return </span>len<span style="font-weight: bold">(</span>list<span style="font-weight: bold">(</span>filter<span style="font-weight: bold">(</span><span style="color: blue; font-weight: bold">lambda </span>x<span style="font-weight: bold">: </span>x <span style="color: blue; font-weight: bold">not in </span>DELIMITERS<span style="font-weight: bold">,
                           </span>itertools<span style="font-weight: bold">.</span>chain<span style="font-weight: bold">(*</span>tokenize_lines<span style="font-weight: bold">(</span>input<span style="font-weight: bold">)))))

</span>@main
<span style="color: blue; font-weight: bold">def </span>run<span style="font-weight: bold">(*</span>args<span style="font-weight: bold">):
    </span>file <span style="font-weight: bold">= </span>sys<span style="font-weight: bold">.</span>stdin
    <span style="color: blue; font-weight: bold">if </span>args<span style="font-weight: bold">:
        </span>file <span style="font-weight: bold">= </span>open<span style="font-weight: bold">(</span>args<span style="font-weight: bold">[</span><span style="color: red">0</span><span style="font-weight: bold">], </span><span style="color: red">'r'</span><span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span><span style="color: red">'counted'</span><span style="font-weight: bold">, </span>count_tokens<span style="font-weight: bold">(</span>file<span style="font-weight: bold">), </span><span style="color: red">'non-delimiter tokens'</span><span style="font-weight: bold">)
</span>
</pre>
</body>
</html>