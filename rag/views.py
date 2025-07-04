from django.shortcuts import render, redirect
from .forms import box  
from .mistrally import appy  
from langchain_core.messages import HumanMessage,AIMessage

def home(request):
    global memory
   
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    
    request.session.set_expiry(3600)  

    form = box(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user_input = form.cleaned_data['YOU']
        memory.append(HumanMessage(content=user_input))
        
        l=10 if len(memory)>10 else len(memory)
        print(l)
       
        response =appy(memory[:l])
        bot_response = response
        memory.append(AIMessage(content=bot_response))
       
        request.session['chat_history'].append({
            'user': user_input,
            'bot': bot_response
        })
        request.session.modified = True  

        return redirect('chat')

    context = {
        'chat_history': request.session.get('chat_history', []),
        'form': form
    }

    return render(request, 'chat.html', context)
memory=[]
