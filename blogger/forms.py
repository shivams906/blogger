from django import forms
from blogger.models import Post


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "content",
        )

    def save(self, author):
        return Post.objects.create(
            title=self.cleaned_data["title"],
            content=self.cleaned_data["content"],
            author=author,
        )
