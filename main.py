import sys

from xml.dom.minidom import parse


def get_element_value(child, tag):
    try:
        return child.getElementsByTagName(tag)[0].firstChild.nodeValue
    except:
        return ""


def parse_xml(filename_xml):
    xml = parse(filename_xml)
    results = {
        "summary": {},
        "tests": [],
    }
    # Parse summary
    xml_summary = xml.getElementsByTagName("test-run")[0]
    results["summary"]["total"] = xml_summary.getAttribute("total")
    results["summary"]["passed"] = xml_summary.getAttribute("passed")
    results["summary"]["failed"] = xml_summary.getAttribute("failed")
    results["summary"]["inconclusive"] = xml_summary.getAttribute("inconclusive")
    results["summary"]["skipped"] = xml_summary.getAttribute("skipped")
    results["summary"]["asserts"] = xml_summary.getAttribute("asserts")
    results["summary"]["date"] = xml_summary.getAttribute("start-time")
    results["summary"]["duration"] = xml_summary.getAttribute("duration")
    # Parse tests
    for child in xml.getElementsByTagName("test-case"):
        results["tests"].append({
            "name": child.getAttribute("fullname"),
            "result": child.getAttribute("result"),
            "duration": child.getAttribute("duration"),
            "message": get_element_value(child, "message"),
            "stack-trace": get_element_value(child, "stack-trace"),
        })
    # Bring failures to top
    for i, item in enumerate(results["tests"]):
        if item["result"] == "Failed":
            results["tests"].insert(0, results["tests"].pop(i))
    return results


def make_github_comment(test_results):

    comment = gh_comment_summary(test_results["summary"])

    failed_tests = [elem for i, elem, in enumerate(test_results["tests"]) if elem["result"] == "Failed"]

    if failed_tests:
        comment += """"
---

### Failed tests:
        """
        comment += gh_comment_failed_details(failed_tests)

    return comment


def gh_comment_summary(test_summary):
    return """### Summary:
<p float="left">
  <img src="https://img.shields.io/badge/Tests-{total}-blue" />
  <img src="https://img.shields.io/badge/Passed-{passed}-green" /> 
  <img src="https://img.shields.io/badge/Failed-{failed}-red" />
  <img src="https://img.shields.io/badge/Inconclusive-{inconclusive}-lightgrey" />
  <img src="https://img.shields.io/badge/Skipped-{skipped}-lightgrey" />
</p>""".format(total=test_summary["total"], passed=test_summary["passed"], failed=test_summary["failed"],
               inconclusive=test_summary["inconclusive"], skipped=test_summary["skipped"])


def gh_comment_failed_details(failed_tests):

    response = ""

    for item in failed_tests:
        response += """*Test:*

**{name}**

*Message:*
```
{message}
```

*Stack Trace:*

```
{stack_trace}
```

---""".format(name=item["name"], message=item["message"], stack_trace=item["stack-trace"])

    return response


def main():
    filename_xml = "example.xml"
    if len(sys.argv) > 1:
        filename_xml = sys.argv[1]
    filename_gh = filename_xml.replace(".xml", "") + "_summary_gh_comment.txt"
    if len(sys.argv) > 2:
        filename_gh = sys.argv[2]
    test_results = parse_xml(filename_xml)
    gh_comment = make_github_comment(test_results)
    file = open(filename_gh, "w")
    file.write(gh_comment)
    file.close()


if __name__ == "__main__":
    main()
