import os
import random

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ملاحظة مهمة عند تعديل الأسئلة:
# الإجابة الصحيحة هي دائمًا "أول عنصر" في قائمة options.
# الخلط (shuffle) يتم على نسخة عند العرض فقط، فلا يتأثر هذا الترتيب.
quiz_data = {
    'title': 'كويز الذكاء الاصطناعي: اختبر معلوماتك 🧠',
    'questions': [
        {
            'id': 1,
            'question_text': 'عند استخدام أدوات الذكاء الاصطناعي المجانية ورفع صور أو ملفات عليها، ما هو الوضع الافتراضي لبياناتك عادة؟',
            'options': [
                'قد تُستخدم في تحسين وتدريب النماذج ما لم تقم بإيقاف ذلك من إعدادات الخصوصية',
                'يتم حذفها نهائياً وأوتوماتيكياً بعد مرور 30 يوماً فقط لأسباب أمنية',
                'تكون مشفرة بالكامل ويستحيل على أي شخص أو نظام الاطلاع عليها نهائياً'
            ],
            'reason': 'الوضع الافتراضي في معظم الخدمات المجانية هو السماح باستخدام المدخلات للتدريب، ولحماية خصوصيتك يجب تعديل إعدادات الحساب (Opt-out).'
        },
        {
            'id': 2,
            'question_text': 'طلبنا معلومة من الذكاء الاصطناعي فأعطانا إجابة مقنعة جداً ومدعومة بأرقام، لكنها غير صحيحة.. ماذا تسمى هذه الظاهرة؟',
            'options': [
                'الهلوسة (Hallucination)، حيث تتنبأ النماذج بالكلمات الأقرب دون التحقق من الحقيقة',
                'القرصنة الرقمية، وتحدث بسبب اختراق السيرفرات وسحب بيانات مغلوطة',
                'التحديث التلقائي، وهو عطل مؤقت يحدث بسبب كثرة الضغط على الخوادم'
            ],
            'reason': 'الهلوسة تعني أن الموديل يبني إجابات بناءً على ترابط الكلمات وليس بحثاً حقيقياً عن الحقائق، مما قد يؤدي لمعلومات وهمية تبدو حقيقية.'
        },
        {
            'id': 3,
            'question_text': 'هل يُعتبر استخدام الحسابات المدفوعة كافياً تماماً لحماية أسرار العمل أو الأكواد السرية للشركات؟',
            'options': [
                'ليس تماماً، فقد تخضع المحادثات أحياناً للمراجعة البشرية لتحسين الأمان وجودة الخدمة',
                'نعم تماماً، لأن الاشتراكات المدفوعة توفر عزلاً كاملاً وسرية تامة بنسبة 100%',
                'نعم تماماً، طالما أنك تقوم بمسح السجل (History) فور انتهائك من العمل'
            ],
            'reason': 'حتى مع الخطط المدفوعة، هناك حالات استثنائية للمراجعة البشرية لتحسين الأنظمة، لذا لا يُنصح برفع معلومات حساسة جداً أو أسرار حرجة.'
        },
        {
            'id': 4,
            'question_text': 'ظهر أمامك فيديو لشخصية مشهورة يتطابق فيه الصوت والصورة بدقة شديدة.. كيف تتأكد من صحة الفيديو بشكل قاطع؟',
            'options': [
                'بالرجوع حصرياً للمصادر الإخبارية والصحف الرسمية الموثوقة للتحقق من الخبر',
                'بالتركيز المكثف على حركة الشفايف ورمش العين لاكتشاف أي خطأ في المونتاج',
                'بمراجعة عدد التفاعلات والمشاركات على الفيديو لمعرفة ما إذا كان حقيقياً أم لا'
            ],
            'reason': 'تقنيات التزييف العميق تطورت لدرجة تختفي معها العيوب البصرية التقليدية، وأصبح الفيصل الحقيقي هو الاعتماد على الأخبار والمصادر الرسمية.'
        },
        {
            'id': 5,
            'question_text': 'طلب الذكاء الاصطناعي بحثاً وكتب لك مراجع وأبحاث علمية بالأسماء وسنة النشر.. ما التصرف الأمثل؟',
            'options': [
                'التحقق من كل مرجع بنفسك على محركات البحث الأكاديمية للتأكد من وجوده فعلياً',
                'اعتمادها مباشرة طالما أن تنسيق المراجع وأرقام الصفحات تبدو احترافية ومنسقة',
                'سؤال الأداة في نفس المحادثة للتأكد: "هل هذه المراجع حقيقية أم مؤلفة؟"'
            ],
            'reason': 'من أشهر عيوب النماذج اختلاق كتب وأبحاث وهمية تبدو واقعية للغاية لتلبية طلب المستخدم، ولذلك يجب مطابقتها يدوياً.'
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
