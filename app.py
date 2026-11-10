import os
import random

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ملاحظة مهمة عند تعديل الأسئلة:
# الإجابة الصحيحة هي دائمًا "أول عنصر" في قائمة options.
# الخلط (shuffle) يتم على نسخة عند العرض فقط، فلا يتأثر هذا الترتيب.
quiz_data = {
    'title': 'كويز الـ AI: فاهم اللعبة ولا بيتعمل عليك نمرة؟ 🧠',
    'questions': [
        {
            'id': 1,
            'question_text': 'لقيت أداة AI مجانية وسريعة جداً قلت أحط عليها صورتك الشخصية أو كلام من الشات الخاص عشان تظبطه.. إيه الفخ الخفي هنا؟',
            'options': [
                'الي بتكتبه بيدخل في تدريب الأداة وممكن تظهر لغيرك، أو تتباع للشركات',
                'الي بتكتبه بيتحفظ مؤقتًا على هارد الموبايل وتتمسح لوحدها بعد ما تقفل التطبيق',
                "ممكن حد يوصل لبياناتك عن طريق خدعة برمجية"
            ],
            'reason': 'المجاني مش دايماً مجاني.. طالما الخدمة ببلاش، فأنت غالباً السلعة و بياناتك بتتدرب بيها الموديلات.'
        },
        {
            'id': 2,
            'question_text': 'سألت الـ AI عن معلومة معينة في مجال تقني دقيق، فرد عليك بكل ثقة وبأرقام وتفاصيل تخليك تصدقه وأنت مغمض.. ليه دي ممكن تكون مصيبة؟',
            'options': [
                'عشان الـ AI بيميل لتأليف إجابات مقنعة وشكلها حقيقي لما بيزنق في معلومة، ودي ظاهرة الهلوسة',
                'عشان الـ AI بيتعمد يدي إجابات غلط عشان يجبرك تشترك في النسخة البروفيشنال الغالية',
                'عشان الـ AI بيكرر كلام قديم ومحدثش السيستم بتاعو صح'
            ],
            'reason': 'الـ AI مبيعرفش يقول "مش عارف"، فبيقوم مألف معلومة من الهوا وبطريقة ثقة تخليك تبلع الطعم.'
        },
        {
            'id': 3,
            'question_text': 'طلبت من الـ AI يعملك فكرة مشروع شخصي سري وتفاصيل خطتك اليومية، هل آمن تسلمه الأسرار دي؟',
             'options': [
                'مش آمن تماماً، لأن الشاتات ممكن تطلع عليها مراجعة بشرية من المطورين أو تتسرب لو السيرفر اتضرب',
                'آمن نسبياً لو عملت سكرين ش็ت ومسحت المحادثة من الأداة فوراً بعد ما تخلص كلام',
                'آمن 100% طالما الحساب متسجل ببريد إلكتروني مش باسمك الحقيقي الصريح'
            ],
            'reason': 'أي حاجة بتحطها في الشات ممكن مهندسو الشركات يشوفوها لأغراض التطوير، فبلاش أسرار حساسة.'
        },
        {
            'id': 4,
            'question_text': 'شوفت فيديو تريند على تيك توك لشخصية مشهورة بتقول كلام غريب جداً وصادم، والفيديو دقيق ومفيش أي غلطة.. تتأكد إزاي؟',
            'options': [
                'تدور بنفسك على المصادر الإخبارية المستقلة، لأن تقنية التزييف العميق بقت مابتسبش أثر واضح بالعين',
                'تركز كويس في حركة الشفايف والإضاءة، لأن التزييف العميق دايماً بيسيب بهتان في الجودات العالية',
                'تعتمد على عدد المشاهدات والريأكتات، لأن الفيديوهات المزيفة بتتكشف وتتقفل في ثواني من المنصة'
            ],
            'reason': 'الـ Deepfake بقى بيطلع بجودة تخدع العين، والمقياس الوحيد هو المصادر الموثوقة مش شكل الفيديو.'
        },
        {
            'id': 5,
            'question_text': 'قلت للـ AI يعملك بحث كامل وكتب لك المراجع بالأسماء، السنين، وحتى أرقام الصفحات بدقة.. تعمل إيه؟',
            'options': [
             "مراجعة المصادر و التتدقيق الزيادة مش هينفعني و ممكن يضلني اكثر فهكتفي لأن المراجع واضح انها دقيقة",
             "تتأكد بدقة برضوا عن طريق أدوات زي google scholar حتي لو واضح انها حقيقية "
             "تسأله تاني هل المراجع صح او لا"
            ],
            'reason': 'من أكبر مقالب الـ AI إنه بيألف مراجع وأبحاث وهمية شكلها علمي جداً وهي من خياله البحت!'
        }
    ]
}

# استخراج الإجابة الصحيحة (أول خيار) + فحص سريع للبيانات عند تشغيل التطبيق
for _q in quiz_data['questions']:
    assert len(set(_q['options'])) == len(
        _q['options']
    ), f"Duplicate options in question {_q['id']}"
    _q['correct_answer'] = _q['options'][0]


@app.route('/')
def home():
    questions = []
    for q in quiz_data['questions']:
        options = q['options'][:]
        random.shuffle(options)
        questions.append({'question_text': q['question_text'], 'options': options})
    return render_template(
        'quiz.html',
        lang='ar',
        title=quiz_data['title'],
        quiz_title=quiz_data['title'],
        questions=questions,
    )


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        return redirect(url_for('home'))

    score = 0
    total_questions = len(quiz_data['questions'])
    detailed_results = []

    for index, question in enumerate(quiz_data['questions']):
        question_key = f'q_{index}'
        user_answer = request.form.get(question_key)
        if user_answer not in question['options']:
            user_answer = None
        is_correct = user_answer == question['correct_answer']

        if is_correct:
            score += 1

        detailed_results.append({
            'question_text': question['question_text'],
            'user_answer': user_answer,
            'correct_answer': question['correct_answer'],
            'is_correct': is_correct,
            'reason': question['reason'],
        })

    return render_template(
        'result.html',
        lang='ar',
        title='نتيجة الكويز',
        score=score,
        total_questions=total_questions,
        detailed_results=detailed_results,
    )

if __name__ == '__main__':
    app.run(debug=False)
