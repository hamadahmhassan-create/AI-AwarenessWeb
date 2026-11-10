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
            'question_text': 'استخدمت أداة AI مجانية من شركة كبيرة ومعروفة، ورفعنا عليها صورك الشخصية أو شغلنا.. إيه الفخ الخفي هنا؟',
            'options': [
                'بياناتك بتدخل افتراضياً في تدريب النماذج الجديدة إلا لو ألغيت الميزة دي يدوياً من الإعدادات',
                'الشركة بتحتفظ بالبيانات لمدة 30 يوم بس للأمان وبعدين بتتمسح نهائي لوحدها',
                'مفيش أي فخ طالما الشركة المطورة للبرنامج عالمية وليها اسم وسمعة كبيرة موثوقة'
            ],
            'reason': 'الشركات الكبرى بتستغل المدخلات المجانية في التدريب كأمر واقع، ولازم الواحد يراجع إعدادات الخصوصية والـ Opt-out بنفسه.'
        },
        {
            'id': 2,
            'question_text': 'سألت الـ AI عن معلومة تقنية معقدة، فرد عليك بكل ثقة وبأرقام ومراجع شكلها حقيقي جداً.. ليه دي ممكن تبقى مصيبة؟',
            'options': [
                'علشان النماذج بتعتمد على توقع الكلام الأقرب للسياق مش جلب حقائق، فبتقوم مؤلفة تفاصيل تبدو مقنعة جداً (الهلوسة)',
                'علشان الـ AI بياخد إجاباته المباشرة من منتديات عشوائية ومبيراجعش وراه نهائي',
                'علشان النسخ المجانية متعمدة تطلع أرقام غلط عشان تضطر تشترك في النسخة المدفوعة'
            ],
            'reason': 'دي ظاهرة "الهلوسة" (Hallucination)؛ الموديل مش باحث ولا بيفكر، ده بيخمن الكلمات اللي ورا بعضها بغض النظر عن صحتها.'
        },
        {
            'id': 3,
            'question_text': 'طلبت من الـ AI يعملك خطة مشروع أو كود برمجي سري لشركتك، هل آمن تحط الأسرار دي؟',
            'options': [
                'مش آمن، لأن المحادثات أحياناً براجعها مهندسون بشر، ومعرضة للتسرب لو السيرفر اتعرض لاختراق',
                'آمن تماماً طالما أنت مشترك في باقة مدفوعة (Paid Plan) ومش بتستخدم النسخة المجانية',
                'آمن طالما مسحت المحادثة من الهيستوري (History) أول ما خلصت شغل وطلعت'
            ],
            'reason': 'حتى الحسابات المدفوعة ممكن تخضع للمراجعة البشرية بغرض تحسين الأمان وجودة الخدمة، فمينفعش تحط أسرار تجارية حساسة.'
        },
        {
            'id': 4,
            'question_text': 'شفت فيديو لشخصية مشهورة بتقول كلام صادم، والصوت والفيديو مظبوطين جداً ومفيش أي غلطة بصرية.. تتأكد إزاي؟',
            'options': [
                'تدور في المواقع الإخبارية والصحف الرسمية، لأن أدوات التزييف العميق بقت تخدع العين تماماً',
                'تركز قوي في حركة الشفايف ورمش العين لأن أدوات الـ Deepfake دايماً بتسيب خطأ صغير في التفاصيل',
                'تشوف عدد المشاهير اللي عملوا شير للفيديو والريأكتات عشان تعرف هو حقيقي ولا تجميعة'
            ],
            'reason': 'تكنولوجيا التزييف العميق اتطورت لدرجة إن العيوب التقليدية اختفت، وبقى الفيصل الوحيد هو المصادر الإخبارية الموثوقة.'
        },
        {
            'id': 5,
            'question_text': 'طلبت من الـ AI يعملك بحث، وكتب لك المراجع بالأسماء والسنين وأرقام الصفحات بدقة غريبة.. تعمل إيه؟',
            'options': [
                'تراجع المراجع بنفسك على محركات بحث علمية، لأن الـ AI بيخترع أبحاث وكتب وأسماء وهمية',
                'تعتمدها علطول طالما أرقام الصفحات وتفاصيل سنة النشر مكتوبة بشكل احترافي ومنسق',
                'تسأل الـ AI في نفس الشات: "متأكد إن المراجع دي مش مؤلفة؟" وهو هيصححها لك لو غلط'
            ],
            'reason': 'من أكبر مقالب النماذج إنها بتألف مراجع وأبحاث شكلها علمي جداً وتخدع أي حد، ولازم تتاكد منها بنفسك.'
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
        user_answer = request.request.form.get(question_key) if hasattr(request, 'form') else request.form.get(question_key)
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
