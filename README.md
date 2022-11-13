# Hacking supervisor slow reload/restart
Supervisord slow reload/restart demo.

## TLDR
Due to supervisor signalling behavior separate programms get signalled one at a time. Groups on the other hand share signals between all workers simultaniuosly. Supervisord will wait for script to exit before starting another task, signalling to other programm or starting another one.

#### Test results

|Reloading 30 tasks w/o group|Reloading 30 tasks with group|
|---|---|
|1m 32.5s|4.85s|

### Some code references
supervisorctls controller plugins [do_signal](https://github.com/Supervisor/supervisor/blob/8b83afdac70f140787fdb160d930f824a1f90a33/supervisor/supervisorctl.py#L918) separate process names and group names and signall them differenly.

RPC on the other side on receiving signal proceeds incoming signal to group processes via `make_all_func` [SignalProcessGroup](https://github.com/Supervisor/supervisor/blob/8b83afdac70f140787fdb160d930f824a1f90a33/supervisor/rpcinterface.py#L520).

### Hacked solution

As of supervisor 4.2.4 `supervisorctl reload` does not accept arguments. So we cannot use [all](https://github.com/Supervisor/supervisor/blob/8b83afdac70f140787fdb160d930f824a1f90a33/supervisor/supervisorctl.py#L911), like with `supervisor restart`.

But we can leverage group notification mechanics.

Simply [creating group](script.conf#387) (not called `all` for unexpected conflicts with supervisorctl hardcoded all) containing all of the programms controlled by supervisord.
This insures that all processes will recieve SIGTERM simultaiously upon reload/restart.

### Benchmark

This repository contains:
- simple python script imitating some real service behavior, upon receiving SIGTERM script will sleep for 3 seconds then exit with rc0.
- dockerized supervisord/supervisorctl.
- sample config imitating 30 different realworldish commands

I've included some `supervisorctl reload` logs [with group enabled](supervisor_with_group.log) and [without](supervisor_wo_group.log) as a worst case scenario.

#### Running benchmark

```
docker compose up -d
docker compose exec supervisor supervisorctl reload
```

upon completion you can examine logs via:

```
docker compose exec supervisor cat /var/log/supervisord.log
```

Now can comment [group](script.conf#387), restart `supervisor` container, rerun benchmark and see results for yourself.
