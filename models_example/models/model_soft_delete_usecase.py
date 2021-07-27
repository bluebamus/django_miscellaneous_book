from django.db import models


class EstimateRequestBoard(CommonModel, SoftDeleteModel):

    ANSWER_CHOICES = (
        (0, "없음"),
        (1, "완료"),
    )

    title = models.CharField(verbose_name="제목", max_length=100)
    content = models.TextField("내용")


"""
@ pytest sample code 

def test_softdelete():
    # Given
    mock_user = User.objects.create(username="Testuser")
    title = "test"
    content = "testcontent"

    achievement = AchievementBoard()
    achievement.title = title
    achievement.content = content
    achievement.owner = mock_user
    achievement.save()

    achievement2 = AchievementBoard()
    achievement2.title = title
    achievement2.content = content
    achievement2.owner = mock_user
    achievement2.save()

    achievement3 = AchievementBoard()
    achievement3.title = title
    achievement3.content = content
    achievement3.owner = mock_user
    achievement3.save()

    # When & Then
    achievement.delete()  # 삭제한다.
    assert 2 == AchievementBoard.objects.count()  # 삭제해서 총 2개

    # When & Then
    achievement.restore()  # 복구한다.
    assert 3 == AchievementBoard.objects.count()  # 복구해서 총 3개
"""
