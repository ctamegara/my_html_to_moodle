import re
import os


path="../test/"




###############################################################
######                      STYLES                       ######
###############################################################





dicstyles={
    "<p1>" : "<p>" ,
    "</p1>" : "</p>",
    "<ul>" : "<ul>" ,
    "</ul>" : "</ul> <br>",
    "<ol>" : "<ol>" ,
    "</ol>" : "</ol><br>",
    "<li>" : '<li style="left-margin:15px">' ,
    "</li>" : '</li>   ',
    "<div-sec>" : "\n<br>\n<h2 style='text-align:center ; background-color : #2B2B2B; color:#AAAAFF; max-width:75%; margin:auto; border : 3px solid #A0A0FF ; border-radius: 15px; padding:10px;'><b>",
    "</div-sec>" : "</b></h2>\n<br>\n",
    "<div-par>" : '\n<br>\n<div>\n<br>\n' ,
    "</div-par>" : "\n<br>\n</div>\n<br>\n",
    "<div-ex>" : '\n<br>\n<div>\n<br>\n' ,
    "</div-ex>" : "\n<br>\n</div>\n<br>\n",
    "<code>" : '<div style="background-color : #202020; color:#D0D0D0; font-family: monospace; font-size: 12px; font-style: normal; font-variant: normal; font-weight: 600; line-height: 20px; width:50%; margin:auto ;padding-left:2%">',
    "</code>" : "</div><br>",
    "<bemph>" : "<b style='color:#A0A0FF'>",
    "</bemph>" : "</b> ",
    "<quizz>":'<div class="container p-3 my-3 bg-dark text-white">',
    "</quizz>":"</div>\n",
    "<q1>" : "<p>",
    "</q1>" : "</p><ul>",
    "<q-block>" : "<div>",
    "</q-block>" : "</ul></div>\n",
    "<a1>":"",
    "</a1>":"",
    "<c>":"",
    "</c>":"",
    "<inlinecode>" : '<span style="background-color : #ABABAB; color:#010101; font-family: monospace; font-size: 12px; font-style: normal; font-variant: normal; font-weight: 500;"> &nbsp;',
    "</inlinecode>" : "&nbsp;</span> ",          
    "<ic>" : '<span style="background-color : #ABABAB; color:#010101; font-family: monospace; font-size: 12px; font-style: normal; font-variant: normal; font-weight: 500;"> &nbsp;',
    "</ic>" : "&nbsp;</span> ",  
    "<dropdown>" : '<div class="container p-3 my-3 bg-dark text-white style="margin:10%;width:80%;border:1px solid #BDBDBD;border-radius:5px;padding:10px;padding-left:25px;">',
    "</dropdown>" : "</div>",         
    
    }


###############################################################
######                PYTHON CODES                       ######
###############################################################


def highlight(code):


    code = code.replace(">", "&gt;")
    code = code.replace(">", "&lt;")

    kw = [  "import ",
            "from ",
            "while ",
            "with ",
            "for ",
            "def ",
            "in ",
            "class ",
            "self",
            "return ",
            "pass",
            "if"]

    #comments
    _def= re.findall(r"\#(.*?)\n", code)
    for w in _def :
        code = code.replace(w, '<span style="color:#B8AAC8">' + w + '</span>')       


    #indent
    code= code.replace("    ","\t")
    code = code.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")

       
    #strings
    _def= re.findall(r'"[^"]*"',code)
    for w in _def:
        code = code.replace(w, '<span style="color:#AC87A5">' + w + "</span>")


    
    code = code.replace("\n","<br>")

    #keywords
    for k in kw:
        code = code.replace(k, '<b style="color:#9D72CA">' + k + '</b>')

    
    _def= re.findall("\w+\(", code)
    _def.sort(key = lambda x : 1-len(x) )
    for w in _def:
        code = code.replace(w, '<b style="color:#BFC469">' + w[:-1] + "</b>(")
        tralala=2
 
    
    return code






###############################################################
######                      DROPDOWNS                    ######
###############################################################




def latex_to_html(text,counterdd) :
    
    A=text.split("$$")
    mms=[A[i] for i in range(len(A)) if i%2==1]
    oths=[A[i] for i in range(len(A)) if i%2==0]
    line=[]
    ms=[]
    texts=[]
    c=0
    for oth in oths :
        c+=1
        B=oth.split("$")
        ms+=[B[i] for i in range(len(B)) if i%2==1]
        texts+=[B[i].replace("\n","<br>") for i in range(len(B)) if i%2==0]
        line+=[i%2 for i in range(len(B))]
        if c<=len(mms) :
            line+=[2]
        prep=""
        ct=0
        for x in line :
            if x==0:
                prep+='<span id="text_{}_{}">  </span>'.format(counterdd,ct)
                ct+=1
            if x==1 :
                prep+="\({{}}\)"
            if x==2 :
                prep+='<p style="text-align:center">  \[{{}}\]  </p>'
    return line, texts, ms, mms , prep

def latex_to_dd(text,counterdd) :
    line, texts, ms, mms, prep=latex_to_html(text,counterdd)
    
    answer="""
    <script> 
    """
    answer+="""
    function dropdown{}() {{
        var line={};
        var texts= {};
        var ms = {};
        var mms={};
        var prep = MathJax.Hub.getAllJax("viewer{}");
        for (let i = 0; i < texts.length; i++) {{
            var k = i;
            var k = "text_{}_" + k.toString();
            a = document.getElementById(k);
            a.innerHTML = texts[i];
        }};
        var c=0;
        var cm=0;
        var cmm=0;
        for (let i = 0; i < line.length; i++) {{
            if (line[c]==0) {{ c+=1; }};
            if (line[c]==1) {{MathJax.Hub.Queue(["Text", prep[i], ms[cm]]); c+=1; cm+=1;}};
            if (line[c]==2) {{MathJax.Hub.Queue(["Text", prep[i], mms[cmm]]);c+=1; cmm+=1;}};
        }};
    }};
    </script>


    <div class="dropdown">
    <button class="btn btn-secondary dropdown-toggle  bg-dark text-white" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" onclick="dropdown{}()">
        see the solution
    </button>
    <div id="viewer{}" class="dropdown-menu p-3 mb-2 bg-secondary text-black" aria-labelledby="dropdownMenuButton" x-placement="bottom-start" style="position: absolute; transform: translate3d(0px, -30px, 0px); top: 0px; left: 0px; will-change: transform;" x-out-of-boundaries="">
    {}
    </div>
    </div>
  """.format(counterdd,line, texts, ms, mms, counterdd,counterdd,counterdd,counterdd,prep)
    return answer



Q_holes="""<div class="container p-3 my-3 bg-dark text-white"><h3 style="color: white"> Problem {} :</h3><br>{}</div>"""










def dd_to_html(text,counterDD):
    answer=re.findall(r"<dda>(.*?)</dda>", text, re.DOTALL)[0]
    answer=latex_to_dd(answer,counterDD) 
    question=re.findall(r"<ddq>(.*?)</ddq>", text, re.DOTALL)[0]
    return Q_holes.format(counterDD,question)+answer
    












###############################################################
######                      QUIZZES                      ######
###############################################################



def quizz_header_and_footer(counterQ, n_Q):
    
    quizz_header="""

<script>
    function submitQuiz_{}() {{

        for( var i=1; i<{}+1;i++){{
            
            document.getElementById('correctAnswer'+i.toString() +'_{}').innerHTML = "";
            }};
        

        function answerScore_{}(qName) {{
            var radiosNo = document.getElementsByName(qName);

            for (var i = 0, length = radiosNo.length; i < length; i++) {{
                if (radiosNo[i].checked) {{
                    var answerValue = Number(radiosNo[i].value);
                }}
            }}
            if (isNaN(answerValue)) {{
                answerValue = 0;
            }}
            return answerValue;
        }}""".format(counterQ,n_Q,counterQ,counterQ)

    quizz_header+="""        
        var calcScore = 0
        var answerscore = 0
        for( var i=1; i<{}+1;i++)
            {{calcScore += answerScore_{}('q'+i.toString() +'_{}');}};

        function correctAnswer(correctStringNo, qNumber) {{
            console.log(correctStringNo);
            return ("The correct answer for question " + qNumber + " was : &nbsp;<strong>" +
                (document.getElementById(correctStringNo).innerHTML) + "</strong>");
        }}""".format(n_Q,counterQ,counterQ)

    quizz_header+="""

        for( var i=1; i<{}+1;i++){{
            if (answerScore_{}('q'+i.toString() +'_{}') === 0) {{
                document.getElementById('correctAnswer'+i.toString() +'_{}').innerHTML = correctAnswer('correctString'+i.toString() +'_{}', i);
            }};
        }};
        

        var questionCountArray = {}; 

        var questionCounter = {};

        var showScore = "Your score: " + calcScore + "/" + questionCounter;
        if (calcScore === questionCounter) {{
            showScore = showScore + "&nbsp; <strong>Perfect !</strong>"
        }};
        document.getElementById('userScore{}').innerHTML = showScore;
    }}

    //$(document).ready(function() {{

        //$('#submitButton').click(function() {{
        //    $(this).addClass('hide');
        //}});

    //}});
</script>
""".format(n_Q,counterQ,counterQ,counterQ,counterQ,n_Q,n_Q,counterQ)
    quizz_footer="""
<div class="submitter">
      <input class="quizSubmit" id="submitButton" onClick="submitQuiz_{}()"
      type="submit" value="Hop !" />
</div>
""".format(counterQ)

    for i in range(1,n_Q+1) :
        quizz_footer+="""
    <div class="quizAnswers" id="correctAnswer{}_{}"></div>
        """.format(i,counterQ)

    quizz_footer+="""

<div>
    <p id="userScore{}" style="text-align:center;font-size: 14px; font-style: normal; font-variant: normal; font-weight: 800;"></p>
</div>
""".format(counterQ)
    return quizz_header, quizz_footer

def answer_to_html(text,counterQ,i) :
        
        correct=re.findall(r"<c>(.*?)</c>", text, re.DOTALL)
        if len(correct)>0:
            for c in correct :
                text=text.replace(c, """<input type="radio" name="q{}_{}" value="1">
                                    <label id="correctString{}_{}">{}</label><br>""".format(str(i),counterQ,str(i),counterQ,c))
        else :
            text=text.replace(text, """<input type="radio" name="q{}_{}" value="0">
                                    <label>{}</label><br>""".format(str(i),counterQ,text))
        return text

def qblock_to_html(text,i,counterQ) :
    question=re.findall(r"<q1>(.*?)</q1>", text, re.DOTALL)
    for q in question :
        
        text=text.replace(q,'<p ><strong> Q{}</strong> {} </p>'.format(str(i),q))
    
    answers=re.findall(r"<a1>(.*?)</a1>", text, re.DOTALL)
    for w in answers :
        text=text.replace("<a1>"+w+"</a1>", "<a1>"+answer_to_html(w,counterQ,i)+"</a1>")
    return text


def quizz_to_html(text,counterQ) :
    qblocks=re.findall(r"<q-block>(.*?)</q-block>", text, re.DOTALL)
    i=0
    for qblock in qblocks :
        i+=1
        text=text.replace(qblock,qblock_to_html(qblock,i,counterQ))
    quizz_header,quizz_footer=quizz_header_and_footer(counterQ, i)
    text=quizz_header+'<h3 style="color: white"> Quiz {} :</h3>'.format(counterQ)+text+quizz_footer
    return text







###############################################################
######                MAIN FUNCTION                      ######
###############################################################



def to_html(text) :
    text='<div style="background-color:#2B2B2B; padding:10px; font-family: monospace; font-size: 14px; color:#DDDDDD;">'+text+'</div>'

    codes=re.findall(r"<code>(.*?)</code>", text, re.DOTALL)
    for w in codes :
        text=text.replace(w,highlight(w))


    dds=re.findall(r"<dropdown>(.*?)</dropdown>", text, re.DOTALL)
    counterDD=0
    for dd in dds :
        counterDD+=1
        text=text.replace(dd,dd_to_html(dd,counterDD))
    
    quizzes=re.findall(r"<quizz>(.*?)</quizz>", text, re.DOTALL)
    counterQ=0
    for q in quizzes :
        counterQ+=1
        text=text.replace(q,quizz_to_html(q,counterQ))
    for z in dicstyles.keys() :
        text=text.replace(z,dicstyles[z])
    return text



def transform(filename):

    with open(path+filename,"r") as f :
        text=f.read()

    with open(path+"tek_"+filename,"w") as f :
        t=to_html(text)
        f.write(t)


transform("Example.html")