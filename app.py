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
            'question_text': 'ضربت معاك في سكة أداة ذكاء اصطناعي مجانية من بتوع الكبار، وقررت ترفع عليها صورك أو شغل الشغل.. إيه بقى المطب اللي هنا؟',
            'options': [
                'داتا بتاعتك بتدخل أوتوماتيك في طاحونة تدريب الموديل، إلا لو أنت دخلت بنفسك وقَفلتها من الإعدادات',
                'الشركة بتشيل الداتا دي وتعملها ديليت بعد ٣٠ يوم بالضبط لأجل الأمان',
                'مفيش أي قلق طالما الموقع ده تبع شركة مشهورة واسمها كبير في السوق'
            ],
            'reason': 'الشركات الكبيرة بتستغل الشغل المجاني اللي بتدخله عشان تطور وتدرب النماذج بتاعتها كوضع افتراضي، فلازم تراجع إعدادات الخصوصية والـ Opt-out كويس.'
        },
        {
            'id': 2,
            'question_text': 'سألت الـ AI سؤال تقني كدة ع الماشي، فراح رد عليك بثقة عمياء وأرقام ومصادر شكلها يوجع البطن من كتر ما هي منسقة.. إيه المشكلة في كده بقى؟',
            'options': [
                'عشان هو مش قاعد بيبحث ولا بيفكر، ده قاعد بيألف حكايات تبدو حقيقية (الهلوسة)',
                "عشان الai بياخد كلامه من مواقع مش شرط تكون موثوقة',
                'عشان النسخ المجانية متبرمجة تطلع أرقام غلط عشان تغلس عليك وتدفع في النسخة البريميوم'
            ],
            'reason': 'دي اللي اسمها "الهلوسة" (Hallucination)؛ الموديل مبيفهمش، هو بيلعب لعبة توقع الكلمات الأقرب لبعضها بغض النظر عن الحقيقة.'
        },
        {
            'id': 3,
            'question_text': 'جت في دماغك فكرة عبقرية وقلت للـ AI يعملك خطة لمشروعك الجديد أو يحطلك الكود السري بتاع الشركة.. هل الحوار ده آمن يا معلم؟',
            'options': [
                'مش آمن خالص، لأن في أحيان كتيرة مهندسين بشر بيراجعوا المحادثات دي، ده غير خطر التسريب لو السيرفرات اضربت',
                'آمن و100 فل و10 طالما أنت دافع ومكتوب جنب حسابك (Paid Plan)',
                'طالما عملت مسح للشات من الهيستوري أول ما خلصت، يبقى مفيش أي أثر للموضوع'
            ],
            'reason': 'حتى لو حسابك مدفوع، البرامج دي أحياناً بتخضع لمراجعة بشرية عشان يظبطوا الأداء والأمان، فما ينفعش تحط أسرارك التجارية وأنت مغمض.'
        },
        {
            'id': 4,
            'question_text': 'ظهر قدامك فيديو لشخصية معروفة بتقول كلام غريب ومستفز، والفيديو والصوت مظبوطين بالمليم ومفيش خيط رفيع يدل على التلاعب.. تتأكد منين بقى؟',
            'options': [
                'تفتح المواقع الإخبارية والصحف المعتمدة، لأن شغل الـ Deepfake بقى بيعدي من تحت العين عادي جداً',
                'تدقق أوي في حركة شفايفه وهو بيتكلم وطريقة رمش عينه، لأن برامج التزييف دي بتسيب غلطة غصب عنها',
                'تبص على عدد الشير والريأكتات والناس اللي عملت كومنتات عشان تعرف الفيديو ده حقيقي ولا فوتوشوب'
            ],
            'reason': 'تكنولوجيا التزييف العميق اتطورت جامد لدرجة إن العيوب القديمة اختفت، والحل الوحيد والأكيد هو إنك ترجع للمصادر الصحفية والرسمية.'
        },
        {
            'id': 5,
            'question_text': 'طلبت من الـ AI يعملك بحث، وكتب لك المراجع بالأسماء والسنين وأرقام الصفحات أكنه دكتور جامعي.. تتصرف إزاي؟',
            'options': [
                'تכנס وتراجع كل مرجع بنفسك ع المواقع الأكاديمية، لأن الـ AI أستاذ في اختراع كتب ومقالات مش موجودة أصلاً',
                'تمشي بيها علطول وتطمن طالما أرقام الصفحات وترتيب السنين مكتوب بشكل مه,ندم واحترافي',
                'تقوله في نفس الشات: "بصراحة كده أنت مؤلف المراجع دي ولا حقيقية؟" وهو هيعترف لك ويظبطها'
            ],
            'reason': 'النماذج دي معروفة باختراعها لـ مراجع وهمية تبدو شكلها حقيقي تماماً عشان تريحك، والحل الوحيد هو الفحص اليدوي.'
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
