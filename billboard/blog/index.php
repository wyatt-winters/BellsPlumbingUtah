<?php
$pageTitle = 'Blog — Utah Boiler Experts | Hydronic Heating Tips, Troubleshooting &amp; Guides';
$pageDesc  = "Boiler troubleshooting, radiant heat guides, snow-melt advice, and homeowner know-how from Utah's hydronic specialists. Updated regularly.";
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title><?= $pageTitle ?></title>
<meta name="description" content="<?= htmlspecialchars($pageDesc) ?>">
<link rel="canonical" href="https://utahboilerexperts.com/blog/">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0B0B0F">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:url" content="https://utahboilerexperts.com/blog/">
<meta property="og:site_name" content="Utah Boiler Experts">
<meta property="og:title" content="<?= $pageTitle ?>">
<meta property="og:description" content="<?= htmlspecialchars($pageDesc) ?>">
<meta property="og:image" content="https://utahboilerexperts.com/images/share.jpg?v=2026-06-15">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/billboard.css">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": ["LocalBusiness", "HVACBusiness"], "@id": "https://utahboilerexperts.com#localbusiness", "name": "Utah Boiler Experts", "telephone": "+1-801-685-3976", "url": "https://utahboilerexperts.com", "address": { "@type": "PostalAddress", "streetAddress": "5212 Chester Rd", "addressLocality": "West Valley City", "addressRegion": "UT", "postalCode": "84120", "addressCountry": "US" } },
    {
      "@type": "Blog",
      "@id": "https://utahboilerexperts.com/blog/#blog",
      "name": "Utah Boiler Experts Blog",
      "description": <?= json_encode($pageDesc) ?>,
      "url": "https://utahboilerexperts.com/blog/",
      "publisher": { "@id": "https://utahboilerexperts.com#localbusiness" }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://utahboilerexperts.com/" },
        { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://utahboilerexperts.com/blog/" }
      ]
    }
  ]
}
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DF82TDY0D7"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-DF82TDY0D7');
</script>
</head>
<?php readfile(__DIR__ . '/../partials/billboard-body.html'); ?>
</html>
