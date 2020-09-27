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
        if self.instance.id != None:
            self.instance.title = self.cleaned_data["title"]
            self.instance.content = self.cleaned_data["content"]
            self.instance.save()
            return self.instance
        else:
            return Post.objects.create(
                title=self.cleaned_data["title"],
                content=self.cleaned_data["content"],
                author=author,
            )
