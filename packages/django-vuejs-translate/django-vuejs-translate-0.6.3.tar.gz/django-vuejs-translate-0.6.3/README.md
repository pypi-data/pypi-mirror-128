# django-vuejs-translate

This project aims to translate messages inside vuejs code.

Initially this idea and code was designed by [Alex Tkachenko](https://gitlab.com/preusx)


### Generating translations

```python
python manage.py jsmakemessages -v3 -e jinja,py,html,js,vue -jse js,vue -i node_modules && python manage.py makemessages -v3 -e jinja,py,html,js,vue -i node_modules
```

### Installation

Update INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'vuejs_translate',
    ...
]
```

Add urls

```python
from django.conf.urls.i18n import i18n_patterns

urlpatterns += i18n_patterns(
    path('vuejs-translate', include('vuejs_translate.urls')),
)
```


Add script to templates

```html
// preferred way to use proxy cache on translations
<script type="text/javascript" src!=exp("hashed_translation_url()")>

// Or use old style with basic url tag
<script type="text/javascript" src!=url('"vuejs_translate:js-i18n"')>

```

Add something like this your js.

```js

import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const messages = { current: window.django.catalog || {} }

Vue.prototype._ = function() {
  return this.$t.apply(this, arguments)
}

export const i18n = new VueI18n({
  locale: 'current',
  messages,
  silentTranslationWarn: true
})

```

### Notes on cache

After 0.6 version library uses cache ONLY for hashed url.

It uses two-level cache system:

1. Every hashed url cached by django for a month.
2. If client ignores headers and sends a fetch - server returns last-modified etag.

You can diable cache with VUEJS_CACHE settings

```
# settings.py

VUEJS_CACHE = False
```
