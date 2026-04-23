# Kilmer

> **val·i·da·tion** /ˌvalɪˈdeɪʃ(ə)n/ *n.*
>
> The action of checking or proving the validity or accuracy of something. 
> *"The validation of test results across multiple datasets."*

Whenever you're introducing a change to [iProc][iProc], you should make sure 
that your current development branch still produces identical results. Any 
differences should be investigated, fixed, and discussed.

Kilmer is a software project that will (hopefully) assist you with iProc 
validation. The idea is simple. Run the same data set through two branches of 
iProc and compare the results. If the results are identical, you're good to 
go. If not...

![Do not pass go][nogo]

Read the official [documentation][Docs] for more.

[iProc]: https://github.com/harvard-nrg/iProc
[Docs]: https://harvard-nrg.github.io/kilmer
[nogo]: docs/images/nogo.png
