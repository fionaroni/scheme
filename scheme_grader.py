<html>
<head>
<title>scheme_grader.py</title>
<link href="css/assignments.css" rel="stylesheet" type="text/css">
</head>

<body>
<h3>scheme_grader.py (<a href="scheme_grader.py">plain text</a>)</h3>
<hr>
<pre>
<span style="color: darkred">"""Automatic grading script for the Scheme project.

Expects the following files in the current directory.

scheme.py
scheme_reader.py
scheme_primitives.py, scheme_tokens.py, scheme_test.py
buffer.py, ucb.py
autograder.py
"""

</span>__version__ <span style="font-weight: bold">= </span><span style="color: red">'1.4'

</span><span style="color: blue; font-weight: bold">from </span>autograder <span style="color: blue; font-weight: bold">import </span>test<span style="font-weight: bold">, </span>run_tests<span style="font-weight: bold">, </span>check_func<span style="font-weight: bold">, </span>check_doctest<span style="font-weight: bold">, </span>test_eval

<span style="color: blue; font-weight: bold">try</span><span style="font-weight: bold">:
    </span><span style="color: blue; font-weight: bold">import </span>scheme<span style="font-weight: bold">, </span>scheme_reader
<span style="color: blue; font-weight: bold">except </span><span style="font-weight: bold">(</span>SyntaxError<span style="font-weight: bold">, </span>IndentationError<span style="font-weight: bold">) </span>as e<span style="font-weight: bold">:
    </span><span style="color: blue; font-weight: bold">import </span>traceback
    <span style="color: blue; font-weight: bold">print</span><span style="font-weight: bold">(</span><span style="color: red">'Unfortunately, the autograder cannot run because ' </span><span style="font-weight: bold">+
          </span><span style="color: red">'your program contains a syntax error:'</span><span style="font-weight: bold">)
    </span>traceback<span style="font-weight: bold">.</span>print_exc<span style="font-weight: bold">(</span>limit<span style="font-weight: bold">=</span><span style="color: red">1</span><span style="font-weight: bold">)
    </span>exit<span style="font-weight: bold">(</span><span style="color: red">1</span><span style="font-weight: bold">)

</span><span style="color: blue; font-weight: bold">import </span>sys
<span style="color: blue; font-weight: bold">from </span>ucb <span style="color: blue; font-weight: bold">import </span>main
<span style="color: blue; font-weight: bold">import </span>scheme_primitives
<span style="color: blue; font-weight: bold">from </span>scheme <span style="color: blue; font-weight: bold">import </span>read_line<span style="font-weight: bold">, </span>Pair<span style="font-weight: bold">, </span>nil<span style="font-weight: bold">, </span>LambdaProcedure<span style="font-weight: bold">, </span>create_global_frame

@test<span style="font-weight: bold">(</span><span style="color: red">'1'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_1<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: red">'3'</span><span style="font-weight: bold">, </span><span style="color: red">3</span><span style="font-weight: bold">),
        (</span><span style="color: red">'-123'</span><span style="font-weight: bold">, -</span><span style="color: red">123</span><span style="font-weight: bold">),
        (</span><span style="color: red">'1.25'</span><span style="font-weight: bold">, </span><span style="color: red">1.25</span><span style="font-weight: bold">),
        (</span><span style="color: red">'true'</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">True</span><span style="font-weight: bold">),
        (</span><span style="color: red">')'</span><span style="font-weight: bold">, </span><span style="color: red">'Error'</span><span style="font-weight: bold">),
        (</span><span style="color: red">"'x"</span><span style="font-weight: bold">, </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'quote'</span><span style="font-weight: bold">, </span><span style="color: red">'x'</span><span style="font-weight: bold">])),
        (</span><span style="color: red">'(quote x)'</span><span style="font-weight: bold">, </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'quote'</span><span style="font-weight: bold">, </span><span style="color: red">'x'</span><span style="font-weight: bold">])),
        (</span><span style="color: red">"'(a b)"</span><span style="font-weight: bold">, </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'quote'</span><span style="font-weight: bold">, [</span><span style="color: red">'a'</span><span style="font-weight: bold">, </span><span style="color: red">'b'</span><span style="font-weight: bold">]])),
        (</span><span style="color: red">"'(a (b c))"</span><span style="font-weight: bold">, </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'quote'</span><span style="font-weight: bold">, [</span><span style="color: red">'a'</span><span style="font-weight: bold">, [</span><span style="color: red">'b'</span><span style="font-weight: bold">, </span><span style="color: red">'c'</span><span style="font-weight: bold">]]])),
        (</span><span style="color: red">"(a (b 'c))"</span><span style="font-weight: bold">, </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'a'</span><span style="font-weight: bold">, [</span><span style="color: red">'b'</span><span style="font-weight: bold">, [</span><span style="color: red">'quote'</span><span style="font-weight: bold">, </span><span style="color: red">'c'</span><span style="font-weight: bold">]]])),
        (</span><span style="color: red">"(a (b '(c d)))"</span><span style="font-weight: bold">, </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'a'</span><span style="font-weight: bold">, [</span><span style="color: red">'b'</span><span style="font-weight: bold">, [</span><span style="color: red">'quote'</span><span style="font-weight: bold">, [</span><span style="color: red">'c'</span><span style="font-weight: bold">, </span><span style="color: red">'d'</span><span style="font-weight: bold">]]]])),
        (</span><span style="color: red">"')"</span><span style="font-weight: bold">, </span><span style="color: red">'Error'</span><span style="font-weight: bold">)
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>catch_syntax_error<span style="font-weight: bold">(</span>read_line<span style="font-weight: bold">), </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'2'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_2<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(a . b)'</span><span style="font-weight: bold">, </span>Pair<span style="font-weight: bold">(</span><span style="color: red">'a'</span><span style="font-weight: bold">, </span><span style="color: red">'b'</span><span style="font-weight: bold">)),
        (</span><span style="color: red">'(a)'</span><span style="font-weight: bold">, </span>Pair<span style="font-weight: bold">(</span><span style="color: red">'a'</span><span style="font-weight: bold">, </span>nil<span style="font-weight: bold">)),
        (</span><span style="color: red">'(a b . c)'</span><span style="font-weight: bold">, </span>Pair<span style="font-weight: bold">(</span><span style="color: red">'a'</span><span style="font-weight: bold">, </span>Pair<span style="font-weight: bold">(</span><span style="color: red">'b'</span><span style="font-weight: bold">, </span><span style="color: red">'c'</span><span style="font-weight: bold">)))
    ]
    </span>tests2 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(a b . c d)'</span><span style="font-weight: bold">, </span><span style="color: red">'Error'</span><span style="font-weight: bold">),
        (</span><span style="color: red">'((a b) (c (d (e f))))'</span><span style="font-weight: bold">,
            </span>pairify<span style="font-weight: bold">([[</span><span style="color: red">'a'</span><span style="font-weight: bold">, </span><span style="color: red">'b'</span><span style="font-weight: bold">], [</span><span style="color: red">'c'</span><span style="font-weight: bold">, [</span><span style="color: red">'d'</span><span style="font-weight: bold">, [</span><span style="color: red">'e'</span><span style="font-weight: bold">, </span><span style="color: red">'f'</span><span style="font-weight: bold">]]]])),
        (</span><span style="color: red">'(a . (b . (c . (d . ()))))'</span><span style="font-weight: bold">,
            </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'a'</span><span style="font-weight: bold">, </span><span style="color: red">'b'</span><span style="font-weight: bold">, </span><span style="color: red">'c'</span><span style="font-weight: bold">, </span><span style="color: red">'d'</span><span style="font-weight: bold">])),
        (</span><span style="color: red">'(. . 2)'</span><span style="font-weight: bold">, </span><span style="color: red">'Error'</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(2 . 3 4 . 5)'</span><span style="font-weight: bold">, </span><span style="color: red">'Error'</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(2 (3 . 4) 5)'</span><span style="font-weight: bold">, </span>Pair<span style="font-weight: bold">(</span><span style="color: red">2</span><span style="font-weight: bold">, </span>Pair<span style="font-weight: bold">(</span>Pair<span style="font-weight: bold">(</span><span style="color: red">3</span><span style="font-weight: bold">, </span><span style="color: red">4</span><span style="font-weight: bold">), </span>Pair<span style="font-weight: bold">(</span><span style="color: red">5</span><span style="font-weight: bold">, </span>nil<span style="font-weight: bold">)))),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>catch_syntax_error<span style="font-weight: bold">(</span>read_line<span style="font-weight: bold">), </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>catch_syntax_error<span style="font-weight: bold">(</span>read_line<span style="font-weight: bold">), </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'3'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_3<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">return </span>check_doctest<span style="font-weight: bold">(</span><span style="color: red">'apply_primitive'</span><span style="font-weight: bold">, </span>scheme<span style="font-weight: bold">)


</span>@test<span style="font-weight: bold">(</span><span style="color: red">'4'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_4<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(+ 2 3)'</span><span style="font-weight: bold">, </span><span style="color: red">5</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(+ 2 3 4 5 6 7)'</span><span style="font-weight: bold">, </span><span style="color: red">27</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(+ 2)'</span><span style="font-weight: bold">, </span><span style="color: red">2</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(+)'</span><span style="font-weight: bold">, </span><span style="color: red">0</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(* (+ 3 2) (+ 1 7))'</span><span style="font-weight: bold">, </span><span style="color: red">40</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(+ (* 3 (+ (* 2 4) (+ 3 5))) (+ (- 10 7) 6))'</span><span style="font-weight: bold">, </span><span style="color: red">57</span><span style="font-weight: bold">),
    ]
    </span>tests2 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(odd? 13)'</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">True</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(car (list 1 2 3 4))'</span><span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">),
        (</span><span style="color: red">'hello'</span><span style="font-weight: bold">, </span><span style="color: red">'SchemeError'</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(car car)'</span><span style="font-weight: bold">, </span><span style="color: red">'SchemeError'</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(odd? 1 2 3)'</span><span style="font-weight: bold">, </span><span style="color: red">'SchemeError'</span><span style="font-weight: bold">),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'5'</span><span style="font-weight: bold">)
</span>@test<span style="font-weight: bold">(</span><span style="color: red">'A5'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_A5<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(define size 2) size'</span><span style="font-weight: bold">, </span><span style="color: red">2</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(define size 2) (* 5 size)'</span><span style="font-weight: bold">, </span><span style="color: red">10</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(define pi 3.14159) (define radius 10) (* pi (* radius radius))'</span><span style="font-weight: bold">,
                                  </span><span style="color: red">314.159</span><span style="font-weight: bold">),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'6'</span><span style="font-weight: bold">)
</span>@test<span style="font-weight: bold">(</span><span style="color: red">'B6'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_B6<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: red">"(list 'a 'b)"</span><span style="font-weight: bold">, </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'a'</span><span style="font-weight: bold">, </span><span style="color: red">'b'</span><span style="font-weight: bold">])),
        (</span><span style="color: red">"(define a 1) (list a 'b)"</span><span style="font-weight: bold">, </span>pairify<span style="font-weight: bold">([</span><span style="color: red">1</span><span style="font-weight: bold">, </span><span style="color: red">'b'</span><span style="font-weight: bold">])),
        (</span><span style="color: red">"(car '(a b c))"</span><span style="font-weight: bold">, </span><span style="color: red">'a'</span><span style="font-weight: bold">),
        (</span><span style="color: red">"(car (car '((a))))"</span><span style="font-weight: bold">, </span><span style="color: red">'a'</span><span style="font-weight: bold">),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'7'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_7<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(begin (+ 2 3) (+ 5 6))'</span><span style="font-weight: bold">, </span><span style="color: red">11</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(begin (display 3) (newline) (+ 2 3))'</span><span style="font-weight: bold">, </span><span style="color: red">5</span><span style="font-weight: bold">),
    ]
    </span>tests2 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(begin (define x 3) x)'</span><span style="font-weight: bold">, </span><span style="color: red">3</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(define 0 1)'</span><span style="font-weight: bold">, </span><span style="color: red">'SchemeError'</span><span style="font-weight: bold">),
        (</span><span style="color: red">"(begin 30 'hello)"</span><span style="font-weight: bold">, </span><span style="color: red">'hello'</span><span style="font-weight: bold">),
        (</span><span style="color: red">"(begin (define x 3) (cons x '(y z)))"</span><span style="font-weight: bold">, </span>pairify<span style="font-weight: bold">([</span><span style="color: red">3</span><span style="font-weight: bold">, </span><span style="color: red">'y'</span><span style="font-weight: bold">, </span><span style="color: red">'z'</span><span style="font-weight: bold">])),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'8'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_8<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(lambda (x y) (+ x y))'</span><span style="font-weight: bold">,
         </span>LambdaProcedure<span style="font-weight: bold">(</span>pairify<span style="font-weight: bold">([</span><span style="color: red">'x'</span><span style="font-weight: bold">, </span><span style="color: red">'y'</span><span style="font-weight: bold">]),
                         </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'+'</span><span style="font-weight: bold">, </span><span style="color: red">'x'</span><span style="font-weight: bold">, </span><span style="color: red">'y'</span><span style="font-weight: bold">]),
                         </span>create_global_frame<span style="font-weight: bold">()))
    ]
    </span>tests2 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(lambda (x) (+ x) (+ x x))'</span><span style="font-weight: bold">,
         </span>LambdaProcedure<span style="font-weight: bold">(</span>pairify<span style="font-weight: bold">([</span><span style="color: red">'x'</span><span style="font-weight: bold">]),
                         </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'begin'</span><span style="font-weight: bold">, [</span><span style="color: red">'+'</span><span style="font-weight: bold">, </span><span style="color: red">'x'</span><span style="font-weight: bold">], [</span><span style="color: red">'+'</span><span style="font-weight: bold">, </span><span style="color: red">'x'</span><span style="font-weight: bold">, </span><span style="color: red">'x'</span><span style="font-weight: bold">]]),
                         </span>create_global_frame<span style="font-weight: bold">())),
        (</span><span style="color: red">'(begin (define x (lambda () 2)) x)'</span><span style="font-weight: bold">,
         </span>LambdaProcedure<span style="font-weight: bold">(</span>nil<span style="font-weight: bold">,
                         </span><span style="color: red">2</span><span style="font-weight: bold">,
                         </span>create_global_frame<span style="font-weight: bold">())),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'9'</span><span style="font-weight: bold">)
</span>@test<span style="font-weight: bold">(</span><span style="color: red">'A9'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_A9<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(begin (define (f x y) (+ x y)) f)'</span><span style="font-weight: bold">,
            </span>LambdaProcedure<span style="font-weight: bold">(</span>pairify<span style="font-weight: bold">([</span><span style="color: red">'x'</span><span style="font-weight: bold">, </span><span style="color: red">'y'</span><span style="font-weight: bold">]),
                            </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'+'</span><span style="font-weight: bold">, </span><span style="color: red">'x'</span><span style="font-weight: bold">, </span><span style="color: red">'y'</span><span style="font-weight: bold">]),
                            </span>create_global_frame<span style="font-weight: bold">())),
        (</span><span style="color: red">'(begin (define (f) (+ 2 2)) f)'</span><span style="font-weight: bold">,
            </span>LambdaProcedure<span style="font-weight: bold">(</span>nil<span style="font-weight: bold">,
                            </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'+'</span><span style="font-weight: bold">, </span><span style="color: red">2</span><span style="font-weight: bold">, </span><span style="color: red">2</span><span style="font-weight: bold">]),
                            </span>create_global_frame<span style="font-weight: bold">())),
        (</span><span style="color: red">'(begin (define (f x) (* x x)) f)'</span><span style="font-weight: bold">,
            </span>LambdaProcedure<span style="font-weight: bold">(</span>pairify<span style="font-weight: bold">([</span><span style="color: red">'x'</span><span style="font-weight: bold">]),
                            </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'*'</span><span style="font-weight: bold">, </span><span style="color: red">'x'</span><span style="font-weight: bold">, </span><span style="color: red">'x'</span><span style="font-weight: bold">]),
                            </span>create_global_frame<span style="font-weight: bold">())),
        (</span><span style="color: red">'(begin (define (f x) 1 2) f)'</span><span style="font-weight: bold">,
            </span>LambdaProcedure<span style="font-weight: bold">(</span>pairify<span style="font-weight: bold">([</span><span style="color: red">'x'</span><span style="font-weight: bold">]),
                            </span>pairify<span style="font-weight: bold">([</span><span style="color: red">'begin'</span><span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">, </span><span style="color: red">2</span><span style="font-weight: bold">]),
                            </span>create_global_frame<span style="font-weight: bold">())),
        (</span><span style="color: red">'(define (0 x) (* x x))'</span><span style="font-weight: bold">, </span><span style="color: red">'SchemeError'</span><span style="font-weight: bold">),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'10'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_10<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>gf <span style="font-weight: bold">= </span>create_global_frame<span style="font-weight: bold">()

    </span>formals<span style="font-weight: bold">, </span>vals <span style="font-weight: bold">= </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(a b c)'</span><span style="font-weight: bold">), </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(1 2 3)'</span><span style="font-weight: bold">)
    </span>call_frame <span style="font-weight: bold">= </span>gf<span style="font-weight: bold">.</span>make_call_frame<span style="font-weight: bold">(</span>formals<span style="font-weight: bold">, </span>vals<span style="font-weight: bold">)
    </span>doctest <span style="font-weight: bold">= [
        (</span>set<span style="font-weight: bold">(</span>call_frame<span style="font-weight: bold">.</span>bindings<span style="font-weight: bold">), {</span><span style="color: red">'a'</span><span style="font-weight: bold">, </span><span style="color: red">'b'</span><span style="font-weight: bold">, </span><span style="color: red">'c'</span><span style="font-weight: bold">}),
        (</span>len<span style="font-weight: bold">(</span>call_frame<span style="font-weight: bold">.</span>bindings<span style="font-weight: bold">), </span><span style="color: red">3</span><span style="font-weight: bold">),
        (</span>call_frame<span style="font-weight: bold">.</span>bindings<span style="font-weight: bold">[</span><span style="color: red">'a'</span><span style="font-weight: bold">], </span><span style="color: red">1</span><span style="font-weight: bold">),
        (</span>call_frame<span style="font-weight: bold">.</span>bindings<span style="font-weight: bold">[</span><span style="color: red">'b'</span><span style="font-weight: bold">], </span><span style="color: red">2</span><span style="font-weight: bold">),
        (</span>call_frame<span style="font-weight: bold">.</span>bindings<span style="font-weight: bold">[</span><span style="color: red">'c'</span><span style="font-weight: bold">], </span><span style="color: red">3</span><span style="font-weight: bold">),
        (</span>call_frame<span style="font-weight: bold">.</span>parent<span style="font-weight: bold">, </span>gf<span style="font-weight: bold">),
        ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span><span style="color: blue; font-weight: bold">lambda </span>x<span style="font-weight: bold">: </span>x<span style="font-weight: bold">, </span>doctest<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

    </span>formals <span style="font-weight: bold">= </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(a b c)'</span><span style="font-weight: bold">)
    </span>args <span style="font-weight: bold">= </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(2 #t a)'</span><span style="font-weight: bold">)
    </span>lf <span style="font-weight: bold">= </span>gf<span style="font-weight: bold">.</span>make_call_frame<span style="font-weight: bold">(</span>formals<span style="font-weight: bold">, </span>args<span style="font-weight: bold">)
    </span>tests1 <span style="font-weight: bold">= [
        (</span>lf<span style="font-weight: bold">.</span>bindings<span style="font-weight: bold">[</span><span style="color: red">'a'</span><span style="font-weight: bold">], </span><span style="color: red">2</span><span style="font-weight: bold">),
        (</span>lf<span style="font-weight: bold">.</span>bindings<span style="font-weight: bold">[</span><span style="color: red">'b'</span><span style="font-weight: bold">], </span><span style="color: blue; font-weight: bold">True</span><span style="font-weight: bold">),
        (</span>lf<span style="font-weight: bold">.</span>bindings<span style="font-weight: bold">[</span><span style="color: red">'c'</span><span style="font-weight: bold">], </span><span style="color: red">'a'</span><span style="font-weight: bold">),
        (</span>lf<span style="font-weight: bold">.</span>parent<span style="font-weight: bold">, </span>gf<span style="font-weight: bold">),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span><span style="color: blue; font-weight: bold">lambda </span>x<span style="font-weight: bold">: </span>x<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

    </span>formals <span style="font-weight: bold">= </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(a)'</span><span style="font-weight: bold">)
    </span>args <span style="font-weight: bold">= </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(seven)'</span><span style="font-weight: bold">)
    </span>lf2 <span style="font-weight: bold">= </span>lf<span style="font-weight: bold">.</span>make_call_frame<span style="font-weight: bold">(</span>formals<span style="font-weight: bold">, </span>args<span style="font-weight: bold">)
    </span>tests2 <span style="font-weight: bold">= [
        (</span>lf<span style="font-weight: bold">.</span>bindings<span style="font-weight: bold">[</span><span style="color: red">'a'</span><span style="font-weight: bold">], </span><span style="color: red">2</span><span style="font-weight: bold">),
        (</span>lf<span style="font-weight: bold">.</span>parent<span style="font-weight: bold">, </span>gf<span style="font-weight: bold">),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span><span style="color: blue; font-weight: bold">lambda </span>x<span style="font-weight: bold">: </span>x<span style="font-weight: bold">, </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'11'</span><span style="font-weight: bold">)
</span>@test<span style="font-weight: bold">(</span><span style="color: red">'B11'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_B11<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span><span style="color: green; font-style: italic"># Note: Doesn't check well-formed but unrequired list matching.
    # E.g., (lambda (a . b) 2) and (lambda x 2)
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(lambda (x y z) x)'</span><span style="font-weight: bold">,
            </span>LambdaProcedure<span style="font-weight: bold">(</span>pairify<span style="font-weight: bold">([</span><span style="color: red">'x'</span><span style="font-weight: bold">, </span><span style="color: red">'y'</span><span style="font-weight: bold">, </span><span style="color: red">'z'</span><span style="font-weight: bold">]),
                            </span><span style="color: red">'x'</span><span style="font-weight: bold">,
                            </span>create_global_frame<span style="font-weight: bold">())),
        (</span><span style="color: red">'(lambda (0 y z) x)'</span><span style="font-weight: bold">, </span><span style="color: red">'SchemeError'</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(lambda (x y nil) x)'</span><span style="font-weight: bold">, </span><span style="color: red">'SchemeError'</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(lambda (x y (and z)) x)'</span><span style="font-weight: bold">, </span><span style="color: red">'SchemeError'</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(lambda (x #t z) x)'</span><span style="font-weight: bold">, </span><span style="color: red">'SchemeError'</span><span style="font-weight: bold">),
    ]
    </span>tests2 <span style="font-weight: bold">= [
        (</span><span style="color: red">"(lambda (h e l l o) 'world)"</span><span style="font-weight: bold">, </span><span style="color: red">'SchemeError'</span><span style="font-weight: bold">),
        (</span><span style="color: red">"(lambda (c s 6 1 a) 'yay)"</span><span style="font-weight: bold">, </span><span style="color: red">'SchemeError'</span><span style="font-weight: bold">),
        ]

    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'12'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_12<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(define (square x) (* x x)) (square 21)'</span><span style="font-weight: bold">,
            </span><span style="color: red">441</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(define square (lambda (x) (* x x))) (square (square 21))'</span><span style="font-weight: bold">,
            </span><span style="color: red">194481</span><span style="font-weight: bold">),
    ]
    </span>tests2 <span style="font-weight: bold">= [
        (</span><span style="color: darkred">"""(define square (lambda (x) (* x x)))
                 (define (sum-of-squares x y)
                   (+ (square x) (square y)))
                 (sum-of-squares 3 4)"""</span><span style="font-weight: bold">,
            </span><span style="color: red">25</span><span style="font-weight: bold">) ,
        (</span><span style="color: darkred">"""(define double (lambda (x) (* 2 x)))
                 (define compose (lambda (f g) (lambda (x) (f (g x)))))
                 (define apply-twice (lambda (f) (compose f f)))
                 ((apply-twice double) 5)"""</span><span style="font-weight: bold">,
            </span><span style="color: red">20</span><span style="font-weight: bold">),
        (</span><span style="color: darkred">"""(define (outer x y)
                  (define (inner z x)
                    (list x y z))
                  (inner x 10))
                 (outer 1 2)"""</span><span style="font-weight: bold">,
            </span>pairify<span style="font-weight: bold">([</span><span style="color: red">10</span><span style="font-weight: bold">, </span><span style="color: red">2</span><span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">])),
        (</span><span style="color: darkred">"""(define (outer-func x y)
                  (define (inner z x)
                    (list x y z))
                  inner)
                 ((outer-func 1 2)  1 10)"""</span><span style="font-weight: bold">,
            </span>pairify<span style="font-weight: bold">([</span><span style="color: red">10</span><span style="font-weight: bold">, </span><span style="color: red">2</span><span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">])),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'13'</span><span style="font-weight: bold">)
</span>@test<span style="font-weight: bold">(</span><span style="color: red">'A13'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_A13<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(if #t 1 0)'</span><span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(if #f 1 0)'</span><span style="font-weight: bold">, </span><span style="color: red">0</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(if 1 1 0)'</span><span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">),
        (</span><span style="color: red">"(if 'a 1 0)"</span><span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(if (cons 1 2) 1 0)'</span><span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(if #t 1)'</span><span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(if #f 1)'</span><span style="font-weight: bold">, </span>scheme<span style="font-weight: bold">.</span>okay<span style="font-weight: bold">),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'14'</span><span style="font-weight: bold">)
</span>@test<span style="font-weight: bold">(</span><span style="color: red">'B14'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_B14<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(and)'</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">True</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(and 1 #f)'</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">False</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(and 2 1)'</span><span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(and #f 5)'</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">False</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(and 3 2 #f)'</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">False</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(and 3 2 1)'</span><span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(and 3 #f 5)'</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">False</span><span style="font-weight: bold">),
    ]
    </span>tests2 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(or)'</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">False</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(or 1)'</span><span style="font-weight: bold">, </span><span style="color: red">1</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(or #f)'</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">False</span><span style="font-weight: bold">),
        (</span><span style="color: red">"(or 0 1 2 'a)"</span><span style="font-weight: bold">, </span><span style="color: red">0</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(or #f #f)'</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">False</span><span style="font-weight: bold">),
        (</span><span style="color: red">"(or 'a #f)"</span><span style="font-weight: bold">, </span><span style="color: red">'a'</span><span style="font-weight: bold">),
        (</span><span style="color: red">"(or (&lt; 2 3) (&gt; 2 3) 2 'a)"</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">True</span><span style="font-weight: bold">),
        (</span><span style="color: red">'(or (&lt; 2 3) 2)'</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">True</span><span style="font-weight: bold">),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'15'</span><span style="font-weight: bold">)
</span>@test<span style="font-weight: bold">(</span><span style="color: red">'A15'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_A15<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: darkred">"""(cond ((&gt; 2 3) 5)
                  ((&gt; 2 4) 6)
                  ((&lt; 2 5) 7)
                  (else 8))"""</span><span style="font-weight: bold">,
           </span><span style="color: red">7</span><span style="font-weight: bold">),
        (</span><span style="color: darkred">"""(cond ((&gt; 2 3) 5)
                  ((&gt; 2 4) 6)
                  ((&lt; 2 5) 7))"""</span><span style="font-weight: bold">,
           </span><span style="color: red">7</span><span style="font-weight: bold">),
        (</span><span style="color: darkred">"""(cond ((&gt; 2 3) 5)
                  ((&gt; 2 4) 6)
                  (else 8))"""</span><span style="font-weight: bold">,
           </span><span style="color: red">8</span><span style="font-weight: bold">),
        (</span><span style="color: darkred">"""(cond ((&gt; 2 3) 4 5)
                  ((&gt; 2 4) 5 6)
                  ((&lt; 2 5) 6 7)
                  (else 7 8))"""</span><span style="font-weight: bold">,
           </span><span style="color: red">7</span><span style="font-weight: bold">),
        (</span><span style="color: darkred">"""(cond ((&gt; 2 3) (display 'oops) (newline))
                  (else 9))"""</span><span style="font-weight: bold">,
           </span><span style="color: red">9</span><span style="font-weight: bold">),
        (</span><span style="color: darkred">"""(cond ((&lt; 2 1))
                   ((&gt; 3 2))
                   (else 5))"""</span><span style="font-weight: bold">,
            </span><span style="color: blue; font-weight: bold">True</span><span style="font-weight: bold">),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'16'</span><span style="font-weight: bold">)
</span>@test<span style="font-weight: bold">(</span><span style="color: red">'A16'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_A16<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: darkred">"""(define (square x) (* x x))
                 (define (f x y)
                  (let ((a (+ 1 (* x y)))
                        (b (- 1 y)))
                    (+ (* x (square a))
                       (* y b)
                       (* a b))))
                 (f 3 4)"""</span><span style="font-weight: bold">,
            </span><span style="color: red">456</span><span style="font-weight: bold">),
    ]
    </span>tests2 <span style="font-weight: bold">= [
        (</span><span style="color: darkred">"""(define x 3)
                 (define y 4)

                 (let ((x (+ y 2))
                      (y (+ x 1)))
                  (cons x y))"""</span><span style="font-weight: bold">,
            </span>Pair<span style="font-weight: bold">(</span><span style="color: red">6</span><span style="font-weight: bold">, </span><span style="color: red">4</span><span style="font-weight: bold">)),
        (</span><span style="color: darkred">"""(let ((x 'hello)) x)"""</span><span style="font-weight: bold">,
            </span><span style="color: red">'hello'</span><span style="font-weight: bold">),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'17'</span><span style="font-weight: bold">)
</span>@test<span style="font-weight: bold">(</span><span style="color: red">'B17'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_B17<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: darkred">"""(define f (mu (x) (+ x y)))
                 (define g (lambda (x y) (f (+ x x))))
                 (g 3 7)"""</span><span style="font-weight: bold">,
            </span><span style="color: red">13</span><span style="font-weight: bold">),
        (</span><span style="color: darkred">"""(define g (mu () x))
                 (define (high f x)
                   (f))
                 (high g 2)"""</span><span style="font-weight: bold">,
            </span><span style="color: red">2</span><span style="font-weight: bold">),
    ]
    </span>tests2 <span style="font-weight: bold">= [
        (</span><span style="color: darkred">"""(define (f x) (mu () (lambda (y) (+ x y))))
                 (define (g x) (((f (+ x 1))) (+ x 2)))
                 (g 3)"""</span><span style="font-weight: bold">,
            </span><span style="color: red">8</span><span style="font-weight: bold">),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True


</span>@test<span style="font-weight: bold">(</span><span style="color: red">'18'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_18<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
         (</span><span style="color: red">"(merge &lt; '(1 5 7 9) '(4 8 10))"</span><span style="font-weight: bold">,
          </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(1 4 5 7 8 9 10)'</span><span style="font-weight: bold">)),
         (</span><span style="color: red">"(merge &gt; '(9 7 5 1) '(10 8 4 3))"</span><span style="font-weight: bold">,
          </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(10 9 8 7 5 4 3 1)'</span><span style="font-weight: bold">)),
    ]
    </span>tests2 <span style="font-weight: bold">= [
        (</span><span style="color: red">"(merge &lt; '(1 2 3) '(4))"</span><span style="font-weight: bold">,
         </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(1 2 3 4)'</span><span style="font-weight: bold">)),
        (</span><span style="color: red">"(merge &lt; () '(1 2))"</span><span style="font-weight: bold">,
         </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(1 2)'</span><span style="font-weight: bold">)),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>check_scheme<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>check_scheme<span style="font-weight: bold">, </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True


</span>problem_19_preamble <span style="font-weight: bold">= </span><span style="color: darkred">"""
; True if ss is a list of lists
(define (sol-lol ss)
  (cond ((null? ss) #t)
        ((not (list? ss)) #f)
        ((and (list? (car ss))
              (sol-lol (cdr ss))) #t)
        (else #f)))

; True if ss contains s
(define (sol-contains s ss)
  (and (not (null? ss))
       (or (and (number? s) (= s (car ss)))
           (and (list? s) (sol-contains-all s (car ss)))
           (sol-contains s (cdr ss)))))

; True if ss2 contains all elements of ss1
(define (sol-contains-all ss1 ss2)
  (or (null? ss1)
      (and (sol-contains (car ss1) ss2)
           (sol-contains-all (cdr ss1) ss2))))

; True if ss1 and ss2 are the same list of lists
(define (sol-same-lols ss1 ss2)
  (and (sol-lol ss1)
       (sol-lol ss2)
       (sol-contains-all ss1 ss2)
       (sol-contains-all ss2 ss1)))
"""

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'19'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_19<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: darkred">"""(sol-same-lols (list-partitions 5 2 4)
         '((4 1) (3 2)))"""</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">True</span><span style="font-weight: bold">),
        (</span><span style="color: darkred">"""(sol-same-lols (list-partitions 7 3 5)
         '((5 1 1) (4 2 1) (3 3 1) (3 2 2) (5 2) (4 3)))"""</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">True</span><span style="font-weight: bold">),
        ]
    </span>tests2 <span style="font-weight: bold">= [
        (</span><span style="color: darkred">"""(sol-same-lols (list-partitions 7 2 4)
         '((4 3)))"""</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">True</span><span style="font-weight: bold">),
        (</span><span style="color: darkred">"""(sol-same-lols (list-partitions 7 7 1)
         '((1 1 1 1 1 1 1)))"""</span><span style="font-weight: bold">, </span><span style="color: blue; font-weight: bold">True</span><span style="font-weight: bold">),
    ]
    </span>check <span style="font-weight: bold">= </span><span style="color: blue; font-weight: bold">lambda </span>snippet<span style="font-weight: bold">: </span>check_scheme<span style="font-weight: bold">(</span>snippet<span style="font-weight: bold">, </span>problem_19_preamble<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>check<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>check<span style="font-weight: bold">, </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'20'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_20<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>tests1 <span style="font-weight: bold">= [
        (</span><span style="color: red">'(tree-sums (make-tree 3 nil))'</span><span style="font-weight: bold">,
         </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(3)'</span><span style="font-weight: bold">)),
        (</span><span style="color: red">'(tree-sums tree)'</span><span style="font-weight: bold">,
         </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(20 19 13 16 11)'</span><span style="font-weight: bold">)),
    ]
    </span>tests2 <span style="font-weight: bold">= [
        (</span><span style="color: red">"(tree-sums '(9 (4 (3 (8)) (2)) (5) (1 (2 (6)) (5))))"</span><span style="font-weight: bold">,
         </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(24 15 14 18 15)'</span><span style="font-weight: bold">)),
        (</span><span style="color: red">"(tree-sums '(-3 (-2) (-4)))"</span><span style="font-weight: bold">,
         </span>read_line<span style="font-weight: bold">(</span><span style="color: red">'(-5 -7)'</span><span style="font-weight: bold">)),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>check_scheme<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>check_scheme<span style="font-weight: bold">, </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span>@test<span style="font-weight: bold">(</span><span style="color: red">'22'</span><span style="font-weight: bold">)
</span><span style="color: blue; font-weight: bold">def </span>problem_22<span style="font-weight: bold">(</span>grades<span style="font-weight: bold">):
    </span>scheme<span style="font-weight: bold">.</span>scheme_eval <span style="font-weight: bold">= </span>scheme<span style="font-weight: bold">.</span>scheme_optimized_eval
    tests1 <span style="font-weight: bold">= [
        (</span><span style="color: darkred">"""(define (sum n total)
                   (if (zero? n) total
                     (sum (- n 1) (+ n total))))
                 (sum 1001 0)"""</span><span style="font-weight: bold">,
            </span><span style="color: red">501501</span><span style="font-weight: bold">),
    ]
    </span>tests2 <span style="font-weight: bold">= [
        (</span><span style="color: darkred">"""(define (sum n total)
                   (if (zero? n) total
                     (if #f 42 (sum (- n 1) (+ n total)))))
                 (sum 1001 0)"""</span><span style="font-weight: bold">,
            </span><span style="color: red">501501</span><span style="font-weight: bold">),
    ]
    </span>tests3 <span style="font-weight: bold">= [
        (</span><span style="color: darkred">"""(define (sum n total)
                   (cond ((zero? n) total)
                         ((zero? 0) (sum (- n 1) (+ n total)))
                         (else 42)))
                 (sum 1001 0)"""</span><span style="font-weight: bold">,
            </span><span style="color: red">501501</span><span style="font-weight: bold">),
    ]
    </span>tests4 <span style="font-weight: bold">= [
        (</span><span style="color: darkred">"""(define (sum n total)
                   (if (zero? n) total
                     (add n (+ n total))))
                 (define add (lambda (x+1 y) (sum (- x+1 1) y)))
                 (sum 1001 0)"""</span><span style="font-weight: bold">,
            </span><span style="color: red">501501</span><span style="font-weight: bold">),
    ]
    </span>tests5 <span style="font-weight: bold">= [
        (</span><span style="color: darkred">"""(define (sum n total)
                   (if (zero? n) total
                     (let ((n-1 (- n 1)))
                       (sum n-1 (+ n total)))))
                 (sum 1001 0)"""</span><span style="font-weight: bold">,
            </span><span style="color: red">501501</span><span style="font-weight: bold">),
    ]
    </span><span style="color: blue; font-weight: bold">if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests1<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests2<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests3<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests4<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True
    if </span>check_func<span style="font-weight: bold">(</span>scheme_eval<span style="font-weight: bold">, </span>tests5<span style="font-weight: bold">, </span>comp<span style="font-weight: bold">=</span>scheme_equal<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return True

</span><span style="color: green; font-style: italic">#############
# UTILITIES #
#############

</span><span style="color: blue; font-weight: bold">def </span>pairify<span style="font-weight: bold">(</span>lst<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">if not </span>lst<span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return </span>nil
    <span style="color: blue; font-weight: bold">if </span>type<span style="font-weight: bold">(</span>lst<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">is not </span>list<span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return </span>lst
    <span style="color: blue; font-weight: bold">return </span>Pair<span style="font-weight: bold">(</span>pairify<span style="font-weight: bold">(</span>lst<span style="font-weight: bold">[</span><span style="color: red">0</span><span style="font-weight: bold">]), </span>pairify<span style="font-weight: bold">(</span>lst<span style="font-weight: bold">[</span><span style="color: red">1</span><span style="font-weight: bold">:]))

</span><span style="color: blue; font-weight: bold">def </span>scheme_equal<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span>y<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Are Scheme values x and y equal, even if they use different classes?"""
    </span><span style="color: blue; font-weight: bold">if </span>hasattr<span style="font-weight: bold">(</span>x<span style="font-weight: bold">, </span><span style="color: red">'first'</span><span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">and </span>hasattr<span style="font-weight: bold">(</span>y<span style="font-weight: bold">, </span><span style="color: red">'first'</span><span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">return </span>scheme_equal<span style="font-weight: bold">(</span>x<span style="font-weight: bold">.</span>first<span style="font-weight: bold">, </span>y<span style="font-weight: bold">.</span>first<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">and </span>scheme_equal<span style="font-weight: bold">(</span>x<span style="font-weight: bold">.</span>second<span style="font-weight: bold">, </span>y<span style="font-weight: bold">.</span>second<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">if </span>type<span style="font-weight: bold">(</span>x<span style="font-weight: bold">).</span>__name__ <span style="font-weight: bold">== </span><span style="color: red">'nil' </span><span style="color: blue; font-weight: bold">and </span>type<span style="font-weight: bold">(</span>y<span style="font-weight: bold">).</span>__name__ <span style="font-weight: bold">== </span><span style="color: red">'nil'</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return True
    elif </span>type<span style="font-weight: bold">(</span>x<span style="font-weight: bold">).</span>__name__ <span style="font-weight: bold">== </span><span style="color: red">'LambdaProcedure' </span><span style="color: blue; font-weight: bold">and </span>type<span style="font-weight: bold">(</span>y<span style="font-weight: bold">).</span>__name__ <span style="font-weight: bold">== </span><span style="color: red">'LambdaProcedure'</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">if not </span>environments_equal<span style="font-weight: bold">(</span>x<span style="font-weight: bold">.</span>env<span style="font-weight: bold">, </span>y<span style="font-weight: bold">.</span>env<span style="font-weight: bold">):
            </span><span style="color: blue; font-weight: bold">return False
        return </span>scheme_equal<span style="font-weight: bold">(</span>x<span style="font-weight: bold">.</span>formals<span style="font-weight: bold">, </span>y<span style="font-weight: bold">.</span>formals<span style="font-weight: bold">) </span><span style="color: blue; font-weight: bold">and </span>scheme_equal<span style="font-weight: bold">(</span>x<span style="font-weight: bold">.</span>body<span style="font-weight: bold">, </span>y<span style="font-weight: bold">.</span>body<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">else</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return </span>x <span style="font-weight: bold">== </span>y

<span style="color: blue; font-weight: bold">def </span>environments_equal<span style="font-weight: bold">(</span>env1<span style="font-weight: bold">, </span>env2<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Are environments env1 and env2 equal, even using different classes?"""
    </span><span style="color: blue; font-weight: bold">if </span>type<span style="font-weight: bold">(</span>env1<span style="font-weight: bold">).</span>__name__ <span style="font-weight: bold">!= </span><span style="color: red">'Frame' </span><span style="color: blue; font-weight: bold">or </span>type<span style="font-weight: bold">(</span>env2<span style="font-weight: bold">).</span>__name__ <span style="font-weight: bold">!= </span><span style="color: red">'Frame'</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return False
    if </span>env1<span style="font-weight: bold">.</span>parent <span style="color: blue; font-weight: bold">is </span><span style="color: blue">None </span><span style="color: blue; font-weight: bold">and </span>env2<span style="font-weight: bold">.</span>parent <span style="color: blue; font-weight: bold">is </span><span style="color: blue">None</span><span style="font-weight: bold">:
        </span><span style="color: green; font-style: italic"># Assume that all global frames are the same
        </span><span style="color: blue; font-weight: bold">return True
    if </span>set<span style="font-weight: bold">(</span>env1<span style="font-weight: bold">.</span>bindings<span style="font-weight: bold">) != </span>set<span style="font-weight: bold">(</span>env2<span style="font-weight: bold">.</span>bindings<span style="font-weight: bold">):
        </span><span style="color: green; font-style: italic"># The two environments have different bindings
        </span><span style="color: blue; font-weight: bold">return False
    for </span>binding<span style="font-weight: bold">, </span>value <span style="color: blue; font-weight: bold">in </span>env1<span style="font-weight: bold">.</span>bindings<span style="font-weight: bold">.</span>items<span style="font-weight: bold">():
        </span><span style="color: blue; font-weight: bold">if not </span>scheme_equal<span style="font-weight: bold">(</span>value<span style="font-weight: bold">, </span>env2<span style="font-weight: bold">.</span>bindings<span style="font-weight: bold">[</span>binding<span style="font-weight: bold">]):
            </span><span style="color: blue; font-weight: bold">return False </span><span style="color: green; font-style: italic"># If the values for the same bindings are different
    </span><span style="color: blue; font-weight: bold">return </span>environments_equal<span style="font-weight: bold">(</span>env1<span style="font-weight: bold">.</span>parent<span style="font-weight: bold">, </span>env2<span style="font-weight: bold">.</span>parent<span style="font-weight: bold">)

</span><span style="color: blue; font-weight: bold">def </span>catch_syntax_error<span style="font-weight: bold">(</span>fn<span style="font-weight: bold">):
    </span><span style="color: blue; font-weight: bold">def </span>caught_syntax<span style="font-weight: bold">(*</span>args<span style="font-weight: bold">):
        </span><span style="color: blue; font-weight: bold">try</span><span style="font-weight: bold">:
            </span><span style="color: blue; font-weight: bold">return </span>fn<span style="font-weight: bold">(*</span>args<span style="font-weight: bold">)
        </span><span style="color: blue; font-weight: bold">except </span>SyntaxError<span style="font-weight: bold">:
            </span><span style="color: blue; font-weight: bold">return </span><span style="color: red">'Error'
    </span><span style="color: blue; font-weight: bold">return </span>caught_syntax

<span style="color: blue; font-weight: bold">def </span>scheme_eval<span style="font-weight: bold">(</span>snippet<span style="font-weight: bold">):
    </span><span style="color: darkred">"""Convert snippet into a single expression and scheme_eval it."""
    </span><span style="color: green; font-style: italic"># TODO: figure out how to do this more cleanly
    </span>buf <span style="font-weight: bold">= </span>scheme<span style="font-weight: bold">.</span>buffer_lines<span style="font-weight: bold">(</span>snippet<span style="font-weight: bold">.</span>split<span style="font-weight: bold">(</span><span style="color: red">'\n'</span><span style="font-weight: bold">), </span>show_prompt<span style="font-weight: bold">=</span><span style="color: blue; font-weight: bold">True</span><span style="font-weight: bold">)
    </span>exprs <span style="font-weight: bold">= []
    </span><span style="color: blue; font-weight: bold">try</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">while True</span><span style="font-weight: bold">:
            </span>exprs<span style="font-weight: bold">.</span>append<span style="font-weight: bold">(</span>scheme<span style="font-weight: bold">.</span>scheme_read<span style="font-weight: bold">(</span>buf<span style="font-weight: bold">))
    </span><span style="color: blue; font-weight: bold">except </span>EOFError<span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">pass
    </span>env <span style="font-weight: bold">= </span>scheme<span style="font-weight: bold">.</span>create_global_frame<span style="font-weight: bold">()
    </span><span style="color: blue; font-weight: bold">try</span><span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">for </span>expr <span style="color: blue; font-weight: bold">in </span>exprs<span style="font-weight: bold">[:-</span><span style="color: red">1</span><span style="font-weight: bold">]:
            </span>scheme<span style="font-weight: bold">.</span>scheme_eval<span style="font-weight: bold">(</span>expr<span style="font-weight: bold">, </span>env<span style="font-weight: bold">)
        </span><span style="color: blue; font-weight: bold">return </span>scheme<span style="font-weight: bold">.</span>scheme_eval<span style="font-weight: bold">(</span>exprs<span style="font-weight: bold">[-</span><span style="color: red">1</span><span style="font-weight: bold">], </span>env<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">except </span>scheme<span style="font-weight: bold">.</span>SchemeError as err<span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return </span><span style="color: red">'SchemeError'
    </span><span style="color: blue; font-weight: bold">except </span>BaseException as err<span style="font-weight: bold">:
        </span><span style="color: blue; font-weight: bold">return </span>type<span style="font-weight: bold">(</span>err<span style="font-weight: bold">).</span>__name__ <span style="font-weight: bold">+ </span><span style="color: red">' ' </span><span style="font-weight: bold">+ </span>str<span style="font-weight: bold">(</span>err<span style="font-weight: bold">)

</span>utils <span style="font-weight: bold">= </span><span style="color: darkred">"""
(define (square x) (* x x))

(define (abs x)
  (cond ((&gt; x 0) x)
        ((= x 0) 0)
        ((&lt; x 0) (- x))))

(define (len s)
  (if (eq? s '())
    0
    (+ 1 (len (cdr s)))))

(define (equal? x y)
  (cond ((pair? x) (and (pair? y)
                        (equal? (car x) (car y))
                        (equal? (cdr x) (cdr y))))
        ((null? x) (null? y))
        (else (eq? x y))))

(define (map proc items)
  (if (null? items)
      nil
      (cons (proc (car items))
            (map proc (cdr items)))))

(define (filter predicate sequence)
  (cond ((null? sequence) nil)
        ((predicate (car sequence))
         (cons (car sequence)
               (filter predicate (cdr sequence))))
        (else (filter predicate (cdr sequence)))))

(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

(define (combine f)
  (lambda (x y)
    (if (null? x) nil
      (f (list (car x) (car y))
         ((combine f) (cdr x) (cdr y))))))

(define (memq item x)
  (cond ((null? x) false)
        ((eq? item (car x)) x)
        (else (memq item (cdr x)))))

(define compose (lambda (f g) (lambda (x) (f (g x)))))

"""

</span><span style="color: blue; font-weight: bold">def </span>make_check_scheme<span style="font-weight: bold">(</span>file<span style="font-weight: bold">=</span><span style="color: red">'questions.scm'</span><span style="font-weight: bold">):
    </span><span style="color: darkred">"""Check a Scheme question."""
    </span>with open<span style="font-weight: bold">(</span>file<span style="font-weight: bold">, </span><span style="color: red">'r'</span><span style="font-weight: bold">) </span>as f<span style="font-weight: bold">:
        </span>contents <span style="font-weight: bold">= </span>utils <span style="font-weight: bold">+ </span>f<span style="font-weight: bold">.</span>read<span style="font-weight: bold">()
    </span><span style="color: blue; font-weight: bold">def </span>check_scheme<span style="font-weight: bold">(</span>snippet<span style="font-weight: bold">, </span>preamble<span style="font-weight: bold">=</span><span style="color: red">''</span><span style="font-weight: bold">):
        </span>stuff <span style="font-weight: bold">= </span>contents <span style="font-weight: bold">+ </span>preamble <span style="font-weight: bold">+ </span>snippet
        <span style="color: blue; font-weight: bold">return </span>scheme_eval<span style="font-weight: bold">(</span>stuff<span style="font-weight: bold">)
    </span><span style="color: blue; font-weight: bold">return </span>check_scheme

check_scheme <span style="font-weight: bold">= </span>make_check_scheme<span style="font-weight: bold">()



</span><span style="color: green; font-style: italic">##########################
# COMMAND LINE INTERFACE #
##########################

</span>project_info <span style="font-weight: bold">= {
    </span><span style="color: red">'name'</span><span style="font-weight: bold">: </span><span style="color: red">'Project 4: Scheme'</span><span style="font-weight: bold">,
    </span><span style="color: red">'remote_index'</span><span style="font-weight: bold">: </span><span style="color: red">'http://inst.eecs.berkeley.edu/~cs61a/fa13/proj/scheme/'</span><span style="font-weight: bold">,
    </span><span style="color: red">'autograder_files'</span><span style="font-weight: bold">: [
        </span><span style="color: red">'scheme_grader.py'</span><span style="font-weight: bold">,
        </span><span style="color: red">'scheme_test.py'</span><span style="font-weight: bold">,
        </span><span style="color: red">'autograder.py'</span><span style="font-weight: bold">,
    ],
    </span><span style="color: red">'version'</span><span style="font-weight: bold">: </span>__version__<span style="font-weight: bold">,
}

</span>@main
<span style="color: blue; font-weight: bold">def </span>run<span style="font-weight: bold">(*</span>args<span style="font-weight: bold">):
    </span>run_tests<span style="font-weight: bold">(**</span>project_info<span style="font-weight: bold">)
</span>
</pre>
</body>
</html>