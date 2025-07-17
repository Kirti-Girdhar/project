
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.decorators import api_view

from examapp.serializers import UserDataSerializer
from .models import Result, UserData, question
from rest_framework.response import Response

next=-1
# Create your views here.

@api_view(['GET'])
def sendData(request):
    return HttpResponse("{'id':101,'name':'Sai'}")

@api_view(['GET'])
def getUser(request,uname):
    userdatabd=UserData.objects.get(username=uname)
# select * from userdata where username=uname
    response=Response({"username":userdatabd.username,"password":userdatabd.password,"phone":userdatabd.phone})
    # converting the data into dictionary from JSON
    return response

# to get the data FROM THE DATA BASE using serializer
@api_view(['GET'])
def getUser2(request,uname):
    userdatadb=UserData.objects.get(username=uname)
    userial=UserDataSerializer(userdatadb)
    # it is converting data object into JSON string
    response1=Response(userial.data)
    return response1

# to add the data to the data base
@api_view(['POST'])
def addUser(request):
    userfromclient=request.data
    #JSON string is received from the client and converted to dictionary object. 
    # and automaticallyrun converted api
    UserData.objects.create(username=userfromclient['username'],password=userfromclient['password'],phone=userfromclient['phone'])
    response=Response(userfromclient)
    return response

# to update data
@api_view(['PUT'])
def updateUser(request):
    userfromclient=request.data
    userdatabd=UserData.objects.get(username=userfromclient['username'])
    userdatabd.phone=userfromclient['phone']
    userdatabd.password=userfromclient['password']
    userdatabd.save()
    response=Response(userfromclient)
    return response

@api_view(['DELETE'])
def deleteUser(request,uname):
    UserData.objects.filter(username=uname).delete()
    response=Response("Data Deleted Sucessfully!! ")
    return response

@api_view(['GET'])
def getAllUser(request):
    queryset=UserData.objects.all().values()
    listofuser=list(queryset)
    return Response(listofuser)
    # useri=UserDataSerializer(listofuser)
    # response=Response(useri.data)
    # return response


def showform(request):
    return render(request,"examapp/templates/questionform.html")

def giveMeLogin(request):
    return render(request,"examapp/templates/login.html")

def giveMeRegistration(request):
    return render(request, "examapp/templates/registration.html")

def giveMesubject(request):
    return render(request, "examapp/templates/subject.html")

def giveMeQuestion(request):
    return render(request, "examapp/templates/questionnavigation.html")

def viewquestion(request):
    nofrombrowser=request.GET['qno']
    qdata=question.objects.get(qno=nofrombrowser)
    return render(request, "examapp/templates/questionform.html",{'questiondata':qdata})

def AddQuestion(request):
    no=request.GET['qno']
    que=request.GET['qtext']
    ans=request.GET['answer']
    op1=request.GET['op1']
    op2=request.GET['op2']
    op3=request.GET['op3']
    op4=request.GET['op4']
    subject=request.GET['subject']
    question.objects.create(qno=no,qtext=que,answer=ans,op1=op1,op2=op2,op3=op3,op4=op4,subject=subject)
    return render(request, "examapp/templates/questionform.html",{'message':'Question added successfully'})

def UpdateQuestion(request):
    qdb=question.objects.filter(qno=request.GET['qno'],subject=request.GET['subject'])
    qdb.update(qtext=request.GET['qtext'],answer=request.GET['answer'],op1=request.GET['op1'],op2=request.GET['op2'],op3=request.GET['op3'],op4=request.GET['op4'])
    print(connection.queries)
    return render(request,"examapp/templates/questionform.html",{'message':"Question updated "})

def DeleteQuestion(request):
    question.objects.filter(qno=request.GET['qno'],subject=request.GET['subject']).delete()
    print(connection.queries)
    return render(request, "examapp/templates/questionform.html",{'message':"Question Deleted"})

def register(request):
    userfrombrowser=request.GET['username']
    pswdfrombrowser=request.GET['password']
    phonefrombrowser=request.GET['phone']

    UserData.objects.create(username=userfrombrowser,password=pswdfrombrowser,phone=phonefrombrowser)
    print(connection.queries)
    return render(request, "examapp/templates/login.html",{'message':"you are registered"})

def login(request):
    uname=request.GET["username"]
    pswd=request.GET["password"]
    request.session['usrnmdata']=uname

    try:
        userobj=UserData.objects.get(username=uname)
    except:
        return render(request, "examapp/templates/login.html",{'message':"wrong username"})
    
    if userobj.password==pswd:
        request.session['answer']={}
        request.session['score']=0
        request.session['qno']=-1
        # querySet=question.objects.filter(subject='math').values()  #it will fetch data in the form of a set 
        # listofquestion=list(querySet)   
        # #session can not contain set so we will convert it into list 
        # request.session['listofquestion']=listofquestion

        return render(request, "examapp/templates/subject.html",{"message":"you have logged in successfully "})
    
    else:
        return render(request,"examapp/templates/login.html",{"message":"Wrong password"})

# localhost:8000/examapp/...        to open in diferent browser

def startTest(request):
    request.session['subject']=request.GET['subject']
    queryset=question.objects.filter(subject=request.GET['subject']).values()
    #queryset cannot be hold in the session object so we need to typecast it to list
    #and then store it in the session object
    listofquestions=list(queryset)
    request.session['listofquestions']=listofquestions
    return render(request,'examapp/templates/questionnavigation.html',{'question':listofquestions[0]})

def nextQuestion(request):
    # global next
    # next=next+1
    # print(next)
    allquestion=request.session['listofquestions']
    questionindex=request.session['qno']
    if 'op' in request.GET:
        allanswers=request.session['answer']
        allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]
        #allanswer{1:[1,2+2,4,8],2:[2,6+7,13,12]}
    if(questionindex<len(allquestion)-1):
        request.session['qno']=request.session['qno']+1
        quession=allquestion[request.session['qno']]
    else:
        return render(request,'examapp/templates/questionnavigation.html',{'message':'Click on previous'})

    return render(request,'examapp/templates/questionnavigation.html',{'question':quession})

def previousQuestion(request):
    allanswers=request.session['answer']
    allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]
    allquestion=request.session['listofquestions']
    questionindex=request.session['qno']
    
    if questionindex>0:
        request.session['qno']=request.session['qno']-1
        #qno=2-1
        quession=allquestion[request.session['qno']]
        #quesstion=allquestion[1]
    else:
        return render(request,'examapp/templates/questionnavigation.html',{'message':'click on next'})
    return render(request,'examapp/templates/questionnavigation.html',{'question':quession})

def endexam(request):
    if 'op' in request.GET:
        allanswers=request.session['answer']
        allanswers[request.GET['qno']]=[request.GET['qno'],request.GET['qtext'],request.GET['answer'],request.GET['op']]
        #allanswer{1:[1,2+2,4,8],2:[2,6+7,13,12]}

        responses=request.session['answer']
        allanswers2=responses.values()

        for ans in allanswers2: #output on the console
            print(f'The correct answer is {ans[2]} and the submitted answer is {ans[3]}')
            if ans[2]==ans[3]:
                request.session['score']=request.session['score']+1
        finalscore=request.session['score']
        print(f'The final score is {finalscore}')
        try:
            Result.objects.create(username=request.session['usrnmdata'],subject=request.session['subject'],marks=finalscore)
        except:
            return render(request,'examapp/templates/login.html',{'message':'Use another login'})
    # del finalscore
    
    return render(request,'examapp/templates/score.html',{'finalscore':finalscore,'responses':allanswers2})
