import numpy as np
from numpy.linalg import norm



def SLPG_smooth( obj_fun,  manifold, Xinit = None, maxit= 100, gtol = 1e-5, post_process = True, verbosity = 2, **kwargs):
    kkts = []
    feas = []
    fvals = []

    if Xinit is None:
        Xinit = manifold.Init_point()



    n = manifold._n
    p = manifold._p

    X = Xinit

    X_p = np.zeros( (n,p) )

    fval, gradf = obj_fun(X)

    gradr = manifold.JA(X, gradf)
    L = np.linalg.norm(gradf,'fro') + np.linalg.norm(gradr,'fro')


    for jj in range(maxit):

        

        

        if jj < 3:
            stepsize = 0.01/L
        else:
            stepsize = np.abs( np.sum( S * Y ) / np.sum( Y* Y ) )
            stepsize = np.min( (stepsize, 1e10) )

        X_p = X

        X = X - stepsize * gradr

        X = manifold.A(X)

        S = X - X_p

        fval, gradf = obj_fun(X)
        gradr_p = gradr
        gradr = manifold.JA(X, gradf)
        Y = gradr - gradr_p

        substationarity = np.linalg.norm(gradr, 'fro')
        feasibility = manifold.Feas_eval(X)

        if verbosity == 2 and np.mod(jj,20) == 0:
            print("Iter:{}    fval:{:.3e}   kkts:{:.3e}    feas:{:3e}".format(jj,fval, substationarity, feasibility))

        kkts.append( substationarity )
        feas.append( feasibility )
        fvals.append( fval )



        if substationarity < gtol:
            if verbosity >= 1:
                print("Iter:{}    fval:{:.3e}   kkts:{:.3e}    feas:{:3e}".format(jj,fval, substationarity, feasibility))

            break

    if post_process:
        X = manifold.Post_process(X)
        fval, gradf = obj_fun(X)
        gradr = manifold.JA(X, gradf)
        substationarity = np.linalg.norm(gradr, 'fro')
        feasibility = manifold.Feas_eval(X)

        if verbosity >= 1:
            print("Post-processing")
            print("Iter:{}    fval:{:.3e}   kkts:{:.3e}    feas:{:3e}".format(jj,fval, substationarity, feasibility))


        kkts[-1] = substationarity
        feas[-1] = feasibility
        fvals[-1] = fval


    output_dict = { 'kkts': kkts, 'fvals': fvals, 'fea': feasibility, 'kkt': substationarity, 'fval': fval, 'feas': feas}

    return X, output_dict








def SLPG(obj_fun,  manifold, Xinit = None,  maxit= 100, prox = lambda X, eta:  X, gtol = 1e-5, post_process = True, verbosity = 2, **kwargs):
    # prox(X, eta) compute the solution to \min_{Y}  1/\eta ||Y - X||_F^2 + r(Y)
    
    kkts = []
    feas = []
    fvals = []
    steps = []
    
    if Xinit is None:
        Xinit = manifold.Init_point()


    n = manifold._n
    p = manifold._p

    X = Xinit

    X_p = np.zeros( (n,p) )

    fval, gradf = obj_fun(X)

    gradr = manifold.JA(X, gradf)
    L = np.linalg.norm(gradf,'fro') + np.linalg.norm(gradr,'fro')

    Lambda_r = np.zeros([p,p])
    Lambda_r = Arrow_Hurwicz_SLPG(X, gradr, 0.01/L, prox, Lambda_r, manifold)
    Grad = gradr  + manifold.JC(X,Lambda_r)

    for jj in range(maxit):

        

        

        if jj < 5:
            stepsize = 0.01/L
        else:
            stepsize = np.abs( np.sum( S * S ) / np.sum( S* Y ) )
            stepsize = np.min( (stepsize, 1e10) )

        X_p = X

        steps.append(stepsize)

        X = prox(X - stepsize * (gradr + manifold.JC(X,Lambda_r)), stepsize)

        X = manifold.A(X)

        S = X - X_p

        fval, gradf = obj_fun(X)
        gradr_p = gradr
        Grad_p = Grad
        gradr = manifold.JA(X, gradf)

        stepsize_try = np.average(steps[np.maximum(0,jj-10):])
        stepsize_try = np.minimum(np.maximum(stepsize_try,1e-5/L), 1e10/L)

        tol_AW = 1000* manifold.Feas_eval(X)

        Lambda_r = Arrow_Hurwicz_SLPG(X, gradr, stepsize_try, prox, Lambda_r, manifold, tol = tol_AW)

        Grad = gradr  + manifold.JC(X,Lambda_r)


        # Y = gradr - gradr_p
        Y = Grad - Grad_p


        substationarity = np.linalg.norm(S / stepsize, 'fro')
        feasibility = manifold.Feas_eval(X)

        if verbosity == 2 and np.mod(jj,50) == 0:
            print("Iter:{}    fval:{:.3e}   kkts:{:.3e}    feas:{:3e}".format(jj,fval, substationarity, feasibility))

        kkts.append( substationarity )
        feas.append( feasibility )
        fvals.append( fval )



        if substationarity < gtol:
            if verbosity >= 1:
                print("Iter:{}    fval:{:.3e}   kkts:{:.3e}    feas:{:3e}".format(jj,fval, substationarity, feasibility))

            break

    if post_process:
        X = manifold.Post_process(X)
        fval, gradf = obj_fun(X)
        gradr = manifold.JA(X, gradf)
        # substationarity = np.linalg.norm(gradr, 'fro')
        feasibility = manifold.Feas_eval(X)

        if verbosity >= 1:
            print("Post-processing")
            print("Iter:{}    fval:{:.3e}   kkts:{:.3e}    feas:{:3e}".format(jj,fval, substationarity, feasibility))


        kkts[-1] = substationarity
        feas[-1] = feasibility
        fvals[-1] = fval


    output_dict = { 'kkts': kkts, 'fvals': fvals, 'fea': feasibility, 'kkt': substationarity, 'fval': fval, 'feas': feas}

    return X, output_dict





def Arrow_Hurwicz_SLPG(X, G, eta, prox, Lambda, manifold, tol = 0):
    Lambda_temp = Lambda
    try_stepsize = eta
    
    Z_tmp = X - try_stepsize*G
    for jr in range(5):
        X_try = prox(Z_tmp - try_stepsize* manifold.JC(X,Lambda_temp), try_stepsize)
        D_X = 1/try_stepsize*((X_try - X))
        Lambda_inc = manifold.JC_transpose(X, D_X)
        # print(np.linalg.norm(Lambda_inc,'fro'))
        Lambda_temp = Lambda_temp + Lambda_inc
        if np.linalg.norm(Lambda_inc,'fro') < tol:
            break


    return Lambda_temp





def SLPG_l21( obj_fun,  manifold, Xinit = None, maxit= 100, gamma = 0, gtol = 1e-5, post_process = True, verbosity = 2, **kwargs):
    # gamma is the parameter before the regularization term, i.e. onjective function
    # is f(X) + gamma * ||X||_{2,1}
    def prox(X_input, eta):
    # np.max(X_input, 0)
    # return the proximal operator of \gamma * ||X||_{2,1}
        X_ref = np.sqrt(np.sum(X_input** 2, axis= 1, keepdims= True))
        X_ref_reduce = np.maximum(X_ref - gamma * eta, 0 )
        return (X_ref_reduce/(X_ref + 1e-16) )* X_input

    def generate_Lambda_r(X_input):
        X_ref = 1/ ( 1e-14 + np.sqrt(np.sum(X_input** 2, axis= 1, keepdims= True)) )
        # print(X_input.T @(X_ref * X_input))
        return -X_input.T @(X_ref * X_input)
    
    kkts = []
    feas = []
    fvals = []
    steps = []
    
    if Xinit is None:
        Xinit = manifold.Init_point()


    n = manifold._n
    p = manifold._p

    X = Xinit

    X_p = np.zeros( (n,p) )

    fval, gradf = obj_fun(X)

    gradr = manifold.JA(X, gradf)
    L = np.linalg.norm(gradf,'fro') + np.linalg.norm(gradr,'fro')

    Lambda_r = gamma * generate_Lambda_r(X)
    Grad = gradr  + manifold.JC(X,Lambda_r)

    for jj in range(maxit):

        

        

        if jj < 5:
            stepsize = 0.001/L
        else:
            stepsize = np.abs( np.sum( S * S ) / np.sum( S* Y ) )
            stepsize = np.min( (stepsize, 1e5) )
            # print(stepsize)

        X_p = X

        steps.append(stepsize)

        X = prox(X - stepsize * Grad, stepsize)

        X = manifold.A(X)

        S = X - X_p

        fval, gradf = obj_fun(X)
        gradr_p = gradr
        Grad_p = Grad
        gradr = manifold.JA(X, gradf)

        Lambda_r =  gamma * generate_Lambda_r(X)

        Grad = gradr  + manifold.JC(X,Lambda_r)


        # Y = gradr - gradr_p
        Y = Grad - Grad_p


        substationarity = np.linalg.norm(S/stepsize, 'fro')
        feasibility = manifold.Feas_eval(X)

        if verbosity == 2 and np.mod(jj,50) == 0:
            print("Iter:{}    fval:{:.3e}   kkts:{:.3e}    feas:{:3e}".format(jj,fval, substationarity, feasibility))

        kkts.append( substationarity )
        feas.append( feasibility )
        fvals.append( fval )



        if substationarity < gtol:
            if verbosity >= 1:
                print("Iter:{}    fval:{:.3e}   kkts:{:.3e}    feas:{:3e}".format(jj,fval, substationarity, feasibility))

            break

    if post_process:
        X = manifold.Post_process(X)
        fval, gradf = obj_fun(X)
        gradr = manifold.JA(X, gradf)
        # substationarity = np.linalg.norm(gradr, 'fro')
        feasibility = manifold.Feas_eval(X)

        if verbosity >= 1:
            print("Post-processing")
            print("Iter:{}    fval:{:.3e}   kkts:{:.3e}    feas:{:3e}".format(jj,fval, substationarity, feasibility))


        kkts[-1] = substationarity
        feas[-1] = feasibility
        fvals[-1] = fval


    output_dict = { 'kkts': kkts, 'fvals': fvals, 'fea': feasibility, 'kkt': substationarity, 'fval': fval, 'feas': feas}

    return X, output_dict