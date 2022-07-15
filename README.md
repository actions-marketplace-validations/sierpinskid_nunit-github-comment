Parse Unity's NUnit test results XML and create GH comment with markdown

```
- name: Generate NUnit GH Summary comment 
  uses: sierpinskid/unity-nunit-github-comment@v1
  if: always()
  with:
    inputXmlPath: artifacts/results.xml
    outputHtmlPath: artifacts/gh_comment.txt
```


Inspired by [nunit-html-action](https://github.com/rempelj/nunit-html-action)
