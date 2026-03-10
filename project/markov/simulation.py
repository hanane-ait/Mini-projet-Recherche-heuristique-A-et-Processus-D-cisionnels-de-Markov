import random

def monte_carlo(start_fortune, trials=20000, p=0.5, n_states=7):
    """
    Simulation Monte Carlo avec probabilité de gain asymétrique (Extension E4).
    """
    wins = 0
    total_steps = 0
    goal = n_states - 1
    
    for _ in range(trials):
        fortune = start_fortune
        steps = 0
        while 0 < fortune < goal:
            steps += 1
            if random.random() < p:
                fortune += 1
            else:
                fortune -= 1
        
        if fortune == goal:
            wins += 1
        total_steps += steps
        
    mc_win = wins / trials
    mc_loss = 1 - mc_win
    mc_time = total_steps / trials
    
    return mc_win, mc_loss, mc_time