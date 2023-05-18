import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


# Create your tests here.

class QuestionModelTests(TestCase):
    # 测试未来的时间是否会影响返回值由False变为True
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently()对于question的pub_date返回值为假
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    # 测试过去的时间是否会影响返回值由False变为Ture
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1,
                                                   seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    # 测试最近的时间是否会影响返回值由True变为False
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    # 创建一个建立问题的方法，方便后续调用
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    # 如果没有存在问题项，则显示没有可用的问题存在
    # TestCase存在多种断言的方法，以下例子用了3个
    # 1：assertQuerySetEqual 比较返回值中是否包含
    # 2：assertContains 比较返回值是否
    def test_no_question(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [],
        )

        # 过去的问题将会显示在索引页

    def test_past_question(self):
        # 生成一个已经过去30天的问题
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        print(response.context["latest_question_list"])
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    # 将来的问题将不会显示在
    def test_future_question(self):
        # 生成一个未来30天的问题
        create_question(question_text="Future question.", days=30)
        # 访问`site/polls/`页面
        response = self.client.get(reverse("polls:index"))
        # 返回值中是否包含文本信息
        self.assertContains(response, "No polls are available.")
        # 查询集中比较context的[latest_question_list]是否等于空
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [],
        )

    # 过去的问题和现在的问题同时存在是否指示显示过去的问题
    def test_future_question_and_past_question(self):
        # 生成一个过去30天的问题
        question = create_question(question_text="Past question.", days=-30)
        # 生成一个未来30天的问题
        create_question(question_text="Future question.", days=30)
        # 定义访问页面
        response = self.client.get(reverse("polls:index"))
        # 查询集中context的[latest_question_list]的值是否等于过去的问题
        print(response.context["latest_question_list"])
        self.assertIn(question, response.context['latest_question_list'])

    # 同时测试两个问题
    def test_two_past_question(self):
        question1 = create_question(question_text="Past question1.", days=-30)
        question2 = create_question(question_text="Past question2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        print(response.context["latest_question_list"])
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    # 创建一个未来的问题，并在index主页不显示该问题的情况下，通过URL进行访问，测试是否可以访问
    # 不可以访问页面的响应代码为404
    def test_future_question(self):
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # 创建一个过去的问题，试着通过URL的方式直接访问该问题。
    # 对比返回值收到的question_text是否为定义的"Past Question"
    def test_past_question(self):
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class ChoiceResultsViewTests(TestCase):
    # 创建一个未来的问题，在index主页不显示该问题的情况下，通过URL直接访该问题的投票详情页，测试是否可以访问到
    # 不可访问页面的响应代码为404
    def test_future_question_results(self):
        future_question = create_question(question_text="Future Question.", days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # 创建一个在过去的时间内发布的问题，看看是否可以通过URL直接访问该问题
    def test_past_question_results(self):
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class ChoiceIndexViewTests(TestCase):
    # 创建一个问题，不创建问题的选项，看是否可以在polls显示该问题
    def test_question_no_choice_index(self):
        no_choice_question = create_question(question_text="No Choice Question.", days=0)
        url = reverse("polls:index")
        response = self.client.get(url)
        self.assertNotIn(no_choice_question, response.context['latest_question_list'])

    def test_question_choice_index(self):
        choice_question = create_question(question_text="Choice Question.", days=0)
        choice_question.choice_set.create(choice_text="choice 1")
        response = self.client.get(reverse("polls:index"))
        print(response.context['latest_question_list'])
        self.assertIn(choice_question, response.context['latest_question_list'])