from langchain_openai import ChatOpenAI  # تم التحديث هنا
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os
from django.shortcuts import render

os.environ[
    "OPENAI_API_KEY"] = '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'


def translate_task(chat_language, chat_text):
    template_string = """Translate the text that is delimited by triple backticks \
                    into a language that is {language}. text: ```{text}```
                    """
    prompt_template = ChatPromptTemplate.from_template(template_string)

    user_message = prompt_template.format_messages(
        language=chat_language,
        text=chat_text)

    chat = ChatOpenAI(temperature=0.0)
    user_response = chat.invoke(user_message)  # تم التحديث هنا
    return user_response.content


def customer_feedback(customer_langauge, customer_email):
    template_string = """write response email from customer service to the email that is delimited by triple backticks \
                       into a language that is {language} text: ```{email}```
                       """
    prompt_template = ChatPromptTemplate.from_template(template_string)
    customer_messages = prompt_template.format_messages(
        language=customer_langauge,
        email=customer_email)

    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    customer_response = chat.invoke(customer_messages)  # تم التحديث هنا
    return customer_response.content


def customer_review(customer_review):
    review_template = """\
    For the following text, extract the following information:

    gift: Was the item purchased as a gift for someone else? \
    Answer True if yes, False if not or unknown.

    delivery_days: How many days did it take for the product \
    to arrive? If this information is not found, output -1.

    price_value: Extract any sentences about the value or price,\
    and output them as a comma separated Python list.

    Format the output as JSON with the following keys:
    gift
    delivery_days
    price_value

    text: {text}
    """
    prompt_template = ChatPromptTemplate.from_template(review_template)
    customer_messages = prompt_template.format_messages(text=customer_review)

    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    response = chat.invoke(customer_messages)  # تم التحديث هنا
    return response.content


# باقي الدوال تبقى كما هي بدون تغيير
def translate_text_view(request):
    chat_language = "Arabic"
    if request.method == 'GET':
        chat_text = request.GET.get('message', '')
        chat_language = request.GET.get('lang', '')
    else:
        chat_text = "My name is Abdukarim assistant professor at university of petra"

    processed_text = translate_task(chat_language, chat_text)
    context = {
        'response': processed_text.replace("```", ''),
        'message': chat_text,
    }
    return render(request, context=context, template_name='translate.html')


def email_response_view(request):
    customer_language = "Arabic"
    if request.method == 'POST':
        chat_text = request.POST.get('txtemail', '')
    else:
        chat_text = "اسمي عبدالكريم البنا  اود ان  اسأل عن خدمات  شركة جوجل للمطورين"

    processed_text = customer_feedback(customer_language, chat_text)
    context = {
        'response': processed_text.replace("```", ''),
        'message': chat_text,
    }
    return render(request, context=context, template_name='customer_response.html')


def customer_review_view(request):
    if request.method == 'POST':
        review = request.POST.get('txtemail', '')
    else:
        review = "This leaf blower is pretty amazing. It has four settings: candle blower, gentle breeze, windy city, and tornado. It arrived in two days, just before my wife's anniversary present. I think my wife liked it so much that she was speechless. So far, I've been the only one using it, and I've been using it every other morning to clear the leaves on our lawn. It's slightly more expensive than the other leaf blowers out there, but I think it's worth it for the extra features."

    processed_text = customer_review(review)
    context = {
        'response': processed_text,
        'message': review,
    }
    return render(request, context=context, template_name='customer_review.html')


def index(request):
    return render(request, 'index.html')