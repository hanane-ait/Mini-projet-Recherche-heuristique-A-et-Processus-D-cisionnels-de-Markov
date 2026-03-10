import numpy as np

def get_absorbing_data(p=0.5, n_states=7):
    """
    Génère les matrices Q et R pour une probabilité p (Extension E4).
    États absorbants: 0 et n_states-1.
    """
    q = 1 - p
    transient_count = n_states - 2
    
    # Q : Transitions entre états transitoires
    Q = np.zeros((transient_count, transient_count))
    for i in range(transient_count):
        if i > 0: Q[i, i-1] = q  # Probabilité de perdre
        if i < transient_count - 1: Q[i, i+1] = p  # Probabilité de gagner
        
    # R : Transitions vers les états absorbants (0 et But)
    R = np.zeros((transient_count, 2))
    R[0, 0] = q               # Du premier état vers 0 (ruine)
    R[-1, 1] = p              # Du dernier état transitoire vers le but (gain)
    
    return Q, R

def compute_markov_analysis(p=0.5, n_states=7):
    """
    Calcule les composantes analytiques N, t, B.
    """
    Q, R = get_absorbing_data(p, n_states)
    I = np.eye(len(Q))
    
    # Matrice Fondamentale N = (I - Q)^-1
    N = np.linalg.inv(I - Q)
    
    # Temps moyen avant absorption t = N * 1
    t = np.dot(N, np.ones(len(Q)))
    
    # Probabilités d'absorption B = N * R
    B = np.dot(N, R)
    
    return N, t, B