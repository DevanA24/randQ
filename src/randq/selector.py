def rand_draw(n_list, q_list, rng):
  chosen_name = rng.choice(n_list)
  chosen_question = rng.choice(q_list)

  return (chosen_name ,chosen_question)