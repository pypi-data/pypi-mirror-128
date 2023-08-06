# Changelog

<!--next-version-placeholder-->

## v5.15.0 (2021-11-24)
### Feature
* Remove deprecated and put (#450)

* remove deprecated route and PUT route without BCF routes

* fix some tests

* fix last tests and restore project tree route

* restore BCF tests change

* rename fullUpdate operation ([`5769df5`](https://github.com/bimdata/python-api-client/commit/5769df5195f22e65696b4c46ed1a8ee925634526))
* Add leave project route (#449)

* Add leave project route

* fix roles ([`4d52c51`](https://github.com/bimdata/python-api-client/commit/4d52c51628bf3e977074dfec3d8af51615a13c2d))

### Fix
* Fix semantic release ([`aca3560`](https://github.com/bimdata/python-api-client/commit/aca3560c5d69a91d32be6992c0d8aea1153110b4))
* Fix serializer user project (#448)

Breaking Change:
 -  key to  for GroupUser create view
 - Route pk for userProject views is now UserProject pk and not FosUser pk

Some other change:
- fix serializer of userProject for swagger and libs
- add missing invitation user project from project and group
- fix some test ([`8b5446a`](https://github.com/bimdata/python-api-client/commit/8b5446a58252f767665f6cd3fff59af93baddfbd))
* Add invitation key in UserProject ([`30a8fb5`](https://github.com/bimdata/python-api-client/commit/30a8fb5ad88a6aed47de4bcb69a34cd37702e5ff))
* Get cloud size operation id in openapi ([`d508862`](https://github.com/bimdata/python-api-client/commit/d5088627492eec9d1ea02a8915cfb1d7ed4ce09c))
* Fix list/create methods openAPI ([`7519d93`](https://github.com/bimdata/python-api-client/commit/7519d931205caffc57f964e92e0547714d916304))

## v5.14.0 (2021-09-13)
### Feature
* Serialize user-permissions on documents ([`8597421`](https://github.com/bimdata/python-api-client/commit/859742176f6e0827c170dd8d30c95c254d502fcc))
* Add profile_picture field in user serialization

* add user picture field

* fix user.company, add comment about an edge case ([`45bd37c`](https://github.com/bimdata/python-api-client/commit/45bd37ce3e9ead5bb4050fa2a26a609a64e8ac26))
* Add GED permissions ([`00b987a`](https://github.com/bimdata/python-api-client/commit/00b987af3d7f310c07beb9d30c7354b9e5830d26))
* Allow bigger guids ([#420](https://github.com/bimdata/python-api-client/issues/420)) ([`54b2b09`](https://github.com/bimdata/python-api-client/commit/54b2b090cbbf127cf8ac0f17c3492e6d0e1c7f29))

### Fix
* Allow empty name in raw layers and raw materials ([`b96d9a7`](https://github.com/bimdata/python-api-client/commit/b96d9a7eb1e3828fd2b3f7e9edb558b296d38f0b))
* Allow empty name in raw layers and raw materials ([`c0d6bb6`](https://github.com/bimdata/python-api-client/commit/c0d6bb6f662d3289915da48580553bb2277c7ee7))
* Allow empty name in raw layers and raw materials ([`22e450d`](https://github.com/bimdata/python-api-client/commit/22e450d38322621610ca85750524c94dd197f33c))
* Fix dms-tree group permissions ([`38f8ce5`](https://github.com/bimdata/python-api-client/commit/38f8ce5608ad11f8dd1518a9a901da5ef8779bdd))
* Fix field name and add field to children dms-tree ([#426](https://github.com/bimdata/python-api-client/issues/426)) ([`2881af8`](https://github.com/bimdata/python-api-client/commit/2881af81fb7ae5fe2718f8187ffc5ae350aa4ebd))
