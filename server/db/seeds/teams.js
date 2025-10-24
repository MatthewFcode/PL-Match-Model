/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export async function seed(knex) {
  // Deletes ALL existing entries
  await knex('teams').del()
  await knex('teams').insert([
    { team_name: 'Aston Villa', team_logo: '' },
    { team_name: 'Everton', team_logo: '' },
    { team_name: 'Bournemouth', team_logo: '' },
    { team_name: 'Burnley', team_logo: '' },
    { team_name: 'Tottenham', team_logo: '' },
    { team_name: 'Fulham', team_logo: '' },
    { team_name: 'Sunderland', team_logo: '' },
    { team_name: 'Crystal Palace', team_logo: '' },
    { team_name: 'Brentford', team_logo: '' },
    { team_name: 'Newcastle United', team_logo: '' },
    { team_name: 'Leeds', team_logo: '' },
    { team_name: 'Brighton', team_logo: '' },
    { team_name: 'Wolverhampton Wanderers', team_logo: '' },
    { team_name: 'Liverpool', team_logo: '' },
    { team_name: 'West Ham', team_logo: '' },
    { team_name: 'Manchester City', team_logo: '' },
    { team_name: 'Chelsea', team_logo: '' },
    { team_name: 'Manchester United', team_logo: '' },
    { team_name: 'Nottingham Forest', team_logo: '' },
    {
      team_name: 'Arsenal',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/1021px-Arsenal_FC.svg.png',
    },
  ])
}
