IN DEV

Rendertools
--

remote machine process wrangler

* a simple tool that identifies all machines on your network capable of rendering.
* fifo system user system.
* frontend listing current render jobs, whom sent it and the machines being used.
* frontend listing of what machines have DR spawners currently running.

Installation
--

```
..> cd rendertools
..\rendertools> pipenv install
..\rendertools> pipenv shell

..\rendertools> cd rendertools
..\rendertools\rendertools> python manage.py runserver
```

```
http://localhost:8000/rorender
```
