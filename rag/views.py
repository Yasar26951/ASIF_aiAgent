from django.shortcuts import render, redirect
from .forms import box  # Assuming your form class is named 'box'
from .mistrally import appy  # Import your AI model here
from langchain_core.messages import HumanMessage,AIMessage

def home(request):
    global memory
    # Initialize session storage for chat history
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    # Set session expiry (optional)
    request.session.set_expiry(3600)  # 1 hour

    form = box(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user_input = form.cleaned_data['YOU']
        memory.append(HumanMessage(content=user_input))
        
        l=10 if len(memory)>10 else len(memory)
        print(l)
        # Call your model and get AI response
        response =appy(memory[:l])
        bot_response = response
        memory.append(AIMessage(content=bot_response))
        # Append to session chat history
        request.session['chat_history'].append({
            'user': user_input,
            'bot': bot_response
        })
        request.session.modified = True  # Mark session as changed

        return redirect('chat')

    context = {
        'chat_history': request.session.get('chat_history', []),
        'form': form
    }

    return render(request, 'chat.html', context)
memory=[]
