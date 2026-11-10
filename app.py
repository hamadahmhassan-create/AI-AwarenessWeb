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
            'question_text': 'استخدمت أداة AI مجانية وسريعة وحطيت عليها صورتك أو كلام شخصي عشان تظبطه.. إيه الفخ الخفي هنا؟',
            'options': [
                'بياناتك بتُستخدم في تدريب الAI وممكن تظهر لغيرك أو تتباع للشركات',
                'التطبيق بينزل فيروسات ومخاطر أمنية مباشرة و خطيرة على جهازك',
                'بيتم مسح بياناتك فوراً من السيرفرات بمجرد قفل الشات'
            ],
            'reason': 'طالما الخدمة ببلاش، فأنت وبياناتك السلعة اللي بتتدرب بيها الموديلات.'
        },
        {
            'id': 2,
            'question_text': 'سألت الـ AI عن معلومة تقنية دقيقة، فرد عليك بكل ثقة وبأرقام وتفاصيل تخليك تصدقه.. ليه دي ممكن تكون مصيبة؟',
            'options': [
                'عشان الـ AI بيميل لتأليف إجابات مقنعة وشكلها حقيقي لما بيتزنق ',
                'عشان الـ AI بيتعمد يدي إجابات غلط في النسخة المجانية فقط',
                'عشان الـ AI بيعتمد على بيانات قديمة ومبحدثش معلوماته تلقائياً'
            ],
            'reason': 'الـ AI مبيعرفش يقول "مش عارف"، فبيقوم مألف معلومة بثقة شديدة.'
        },
        {
            'id': 3,
            'question_text': 'طلب من الـ AI يعملك خطة مشروع شخصي سري، هل آمن تسلمه الأسرار دي؟',
            'options': [
                'مش آمن، لأن المحادثات بيشوفها مراجعون بشر وقد تتسرب مع أي اختراق',
                'آمن طالما مسحت المحادثة من الحساب بعد ما خلصت',
                'آمن طالما الحساب متسجل بإيميل وهمي مش باسمك الحقيقي'
            ],
            'reason': 'أي حاجة بتحطها في الشات ممكن مهندسو الشركات يشوفوها لأغراض التطوير.'
        },
        {
            'id': 4,
            'question_text': 'شفت فيديو لتمثيلية أو شخصية مشهورة بتقول كلام صادم، والفيديو دقيق جداً ومفيش غلطة.. تتأكد إزاي؟',
            'options': [
                'تبحث في المصادر الإخبارية الموثوقة، لأن الAI بقى مبيسبش أثر بالعين',
                'تركز في حركة الشفايف والإضاءة لأن أدوات التزييف دايماً بتسيب عيوب واضحة',
                'تعتمد على المشاهدات والريأكتات لأن الفيديوهات المزيفة بتتحظر سريعاً'
            ],
            'reason': 'الـ Deepfake بقى بيطلع بجودة تخدع العين، والمقياس الوحيد هو المصادر الرسمية.'
        },
        {
            'id': 5,
            'question_text': 'طلبت من الـ AI بحث وكتب لك المراجع بالأسماء والسنين وأرقام الصفحات بدقة.. تعمل إيه؟',
            'options': [
                'تراجع المراجع بنفسك على محركات بحث علمية مثل Google Scholar',
                'تعتمدها فوراً طالما التفاصيل وأرقام الصفحات مكتوبة بدقة',
                'تسأل الـ AI نفسه في شات تاني هل المراجع دي حقيقية ولا لأ'
            ],
            'reason': 'من أكبر مقالب الـ AI إنه بيألف مراجع وأبحاث وهمية شكلها علمي جداً!'
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
