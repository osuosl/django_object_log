Changelog
=========

0.6
---

**Changes and bugfixes**

* #5811 - 0.5.1 --> 0.6 south migrations
* #3819 - Allow Log entries to store arbitrary data in addition to
  ``ForeignKeys`` to objects
* #3825 - Allow ``LogActions`` (types) to register a cache processing function
* #5547 - Move log list formatting out of ``LogItem`` formatting
* #6267 - Add generic object detail link
* #6279 - Templates are making too many queries to fetch contenttypes


0.5.1
-----

**Changes and bugfixes**

* #3675 - Migrations are not correctly updating ``LogItem.action_id`` for MySQL


0.5
---

* Initial release
