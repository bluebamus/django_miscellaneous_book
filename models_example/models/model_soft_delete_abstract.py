from django.db import models

# reference : https://velog.io/@kim6515516/%EC%9E%A5%EA%B3%A0%EC%97%90%EC%84%9C-%EB%AA%A8%EB%8D%B8-%EC%86%8C%ED%94%84%ED%8A%B8-%EC%82%AD%EC%A0%9C-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0

# SoftDeleteManage 커스텀 매니저 정의
class SoftDeleteManager(models.Manager):
    use_for_related_fields = (
        True  # 옵션은 기본 매니저로 이 매니저를 정의한 모델이 있을 때 이 모델을 가리키는 모든 관계 참조에서 모델 매니저를 사용할 수 있도록 한다.
    )

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


# Mixin SoftDelete 클래스 정의
class SoftDeleteModel(models.Model):

    deleted_at = models.DateTimeField("삭제일", null=True, default=None)

    class Meta:
        abstract = True  # 상속 할수 있게

    objects = SoftDeleteManager()  # 커스텀 매니저

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        self.save(update_fields=["deleted_at"])

    def restore(self):  # 삭제된 레코드를 복구한다.
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])
