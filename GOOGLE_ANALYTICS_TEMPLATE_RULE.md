# Google Analytics Template Rule

## 📊 **MANDATORY: Google Analytics Tag Required on All Pages**

### **Rule: Every HTML page MUST include Google Analytics tag immediately after `<head>`**

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2573Q8G1WD"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-2573Q8G1WD');
</script>
```

### **Implementation Requirements:**

1. **Placement**: Add immediately after the `<head>` tag
2. **No Exceptions**: All HTML pages must include this tag
3. **Template Files**: Include in all page templates and generators
4. **Verification**: Check that tag is present before committing new pages

### **Files Updated (2025-01-27):**
- ✅ All 83 HTML pages in the project
- ✅ Main pages (index.html, about/, tools/, etc.)
- ✅ All navigator pages (NOC, CLB, Wages)
- ✅ All report pages (Express Entry, OINP, BCPNP, etc.)
- ✅ All news pages (daily, digest, etc.)
- ✅ All template files

### **Template Integration:**

When creating new pages, ensure this tag is included in the `<head>` section:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-2573Q8G1WD"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-2573Q8G1WD');
    </script>
    
    <!-- Other meta tags and CSS -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- ... rest of head content ... -->
</head>
```

### **Script for Future Updates:**

Use `add_google_tag.py` script to add Google Analytics to new files:

```bash
python3 add_google_tag.py
```

### **Verification Checklist:**
- [ ] Google tag is present in `<head>` section
- [ ] Tag ID is correct: `G-2573Q8G1WD`
- [ ] Script loads asynchronously
- [ ] No duplicate tags exist
- [ ] Page loads without errors

---

**Last Updated**: 2025-01-27  
**Total Pages Updated**: 83/86 HTML files  
**Analytics ID**: G-2573Q8G1WD 