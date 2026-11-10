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
            'question_text': 'استخدمت أداة AI مجانية من شركة كبرى ومعروفة، ورفعنا عليها صورك أو ملفات عملك.. إيه الفخ الخفي هنا؟',
            'options': [
                'بياناتك تُستخدم افتراضياً في تدريب النماذج ما لم تقم بإلغاء تفعيل ذلك يدوياً من الإعدادات',
                'الشركة تحتفظ بالبيانات لمدة 30 يوماً فقط للأمان ثم يتم حذفها نهائياً تلقائياً',
                'لا يوجد أي فخ طالما الشركة المطورة للبرنامج شهيرة وذات سمعة عالمية موثوقة'
            ],
            'reason': 'الشركات الكبرى تستخدم المدخلات المجانية للتدريب كأمر افتراضي، ويجب دائماً مراجعة سياسة الخصوصية وإعدادات الـ Opt-out.'
        },
        {
            'id': 2,
            'question_text': 'سألت الـ AI عن معلومة تقنية دقيقة، فرد عليك بكل ثقة وبأرقام ومراجع رسمية شكلها حقيقي جداً.. ليه دي ممكن تكون مصيبة؟',
            'options': [
                'عشان النماذج بتعتمد على التنبؤ بأكثر الكلمات ترابطاً مش جلب حقائق، فبتؤلف تفاصيل تبدو مقنعة جداً (الهلوسة)',
                'عشان الـ AI بياخد إجاباته المباشرة من منتديات ومواقع غير موثوقة ومبيراجعش وراه',
                'عشان النسخ المجانية من الـ AI مبرمجة تعطي أرقام عشوائية عشان تدفعك للاشتراك في النسخة المدفوعة'
            ],
            'reason': 'هذه هي "الهلوسة" (Hallucination)؛ النماذج لا تفكر ولا تبحث، بل تتنبأ بالنص الأقرب للسياق بغض النظر عن دقته.'
        },
        {
            'id': 3,
            'question_text': 'طلبت من الـ AI يعملك خطة مشروع أو كود برمجي سري لشركتك، هل آمن تحط الأسرار دي؟',
            'options': [
                'مش آمن، لأن المحادثات ممكن يراجعها مهندسون بشر في بعض الحالات، ومعرضة للتسرب لو حصل اختراق',
                'آمن جداً طالما أنت بتستخدم حساب مدفوع (Paid Plan) مش مجاني',
                'آمن طالما مسحنا الشات من الهيستوري (History) فوراً بعد ما خلصنا شغل'
            ],
            'reason': 'حتى الحسابات المدفوعة قد تخضع لعمليات مراجعة بشرية لأغراض تحسين الأمان والجودة، ولا يمكن اعتبارها آمنة بنسبة 100% للأسرار التجارية.'
        },
        {
            'id': 4,
            'question_text': 'شفت فيديو لشخصية مشهورة بتقول كلام صادم، والصوت والفيديو دقيقين جداً ومفيش أي عيب بصري ظاهر.. تتأكد إزاي؟',
            'options': [
                'تدور في المواقع الإخبارية والصحف الرسمية، لأن أدوات الـ Deepfake الحالية بقت تخدع العين تماماً',
                'تركز قوي في حركة الشفايف ورمش العين لأن أدوات التزييف دايماً بتسيب خطأ بسيط في التفاصيل الدقيقة',
                'تشوف عدد المشاهير اللي عملوا شير للفيديو والريأكتات عشان تعرف هو حقيقي ولا تجميعة'
            ],
            'reason': 'تكنولوجيا التزييف العميق تطورت لدرجة تختفي معها العيوب البصرية التقليدية، وأصبح الفيصل الوحيد هو التحقق عبر المصادر الإخبارية الموثوقة.'
        },
        {
            'id': 5,
            'question_text': 'طلبت من الـ AI بحث وكتب لك المراجع بالأسماء والسنوات وأرقام الصفحات بدقة متناهية.. تعمل إيه؟',
            'options': [
                'تراجع المراجع بنفسك على محركات بحث علمية، لأن الـ AI بيخترع أبحاث وأسماء كتب ومقالات وهمية',
                'تعتمدها فوراً طالما أرقام الصفحات وتفاصيل سنة النشر مكتوبة بشكل احترافي ومنسق',
                'تسأل الـ AI في نفس الشات: "هل أنت متأكد إن المراجع دي مش مؤلفة؟" وهو هيصححها لك لو غلط'
            ],
            'reason': 'أشهر عيوب النماذج هي اختلاق مراجع علمية تبدو حقيقية تماماً وتخدع الباحثين، ولهذا يجب مطابقتها يدوياً.'
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
