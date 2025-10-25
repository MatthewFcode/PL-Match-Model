// /**
//  * @param { import("knex").Knex } knex
//  * @returns { Promise<void> }
//  */
// export async function seed(knex) {
//   // Deletes ALL existing entries
//   await knex('teams').del()
//   await knex('teams').insert([
//     {
//       team_name: 'Aston Villa',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/f/f9/Aston_Villa_FC_logo.svg',
//     },
//     {
//       team_name: 'Everton',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg',
//     },
//     {
//       team_name: 'Bournemouth',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/e/e5/AFC_Bournemouth_%282013%29.svg',
//     },
//     {
//       team_name: 'Burnley',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/0/02/Burnley_FC_logo.svg',
//     },
//     {
//       team_name: 'Tottenham',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg',
//     },
//     {
//       team_name: 'Fulham',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/e/eb/Fulham_FC_%282022%29_logo.svg',
//     },
//     {
//       team_name: 'Sunderland',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/7/7b/Sunderland_AFC.svg',
//     },
//     {
//       team_name: 'Crystal Palace',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/a/a2/Crystal_Palace_FC_logo.svg',
//     },
//     {
//       team_name: 'Brentford',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_logo.svg',
//     },
//     {
//       team_name: 'Newcastle United',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/5/5e/Newcastle_United_FC.svg',
//     },
//     {
//       team_name: 'Leeds',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/5/58/Leeds_United_F.C._logo.svg',
//     },
//     {
//       team_name: 'Brighton',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/f/f6/Brighton_%26_Hove_Albion_logo.svg',
//     },
//     {
//       team_name: 'Wolverhampton Wanderers',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg',
//     },
//     {
//       team_name: 'Liverpool',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg',
//     },
//     {
//       team_name: 'West Ham',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg',
//     },
//     {
//       team_name: 'Manchester City',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_logo.svg',
//     },
//     {
//       team_name: 'Chelsea',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg',
//     },
//     {
//       team_name: 'Manchester United',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg',
//     },
//     {
//       team_name: 'Nottingham Forest',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/e/e5/Nottingham_Forest_F.C._logo.svg',
//     },
//     {
//       team_name: 'Arsenal',
//       team_logo:
//         'https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg',
//     },
//   ])
// }

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
export async function seed(knex) {
  // Deletes ALL existing entries
  await knex('teams').del()
  await knex('teams').insert([
    {
      team_name: 'Aston Villa',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/f/f9/Aston_Villa_FC_logo.svg',
      stadium_lat: 52.50909,
      stadium_lng: -1.885249,
    },
    {
      team_name: 'Everton',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg',
      stadium_lat: 53.438751,
      stadium_lng: -2.966681,
    },
    {
      team_name: 'Bournemouth',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/e/e5/AFC_Bournemouth_%282013%29.svg',
      stadium_lat: 50.735557,
      stadium_lng: -1.838907,
    },
    {
      team_name: 'Burnley',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/0/02/Burnley_FC_logo.svg',
      stadium_lat: 53.789108,
      stadium_lng: -2.230575,
    },
    {
      team_name: 'Tottenham',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg',
      stadium_lat: 51.604252,
      stadium_lng: -0.067007,
    },
    {
      team_name: 'Fulham',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/e/eb/Fulham_FC_%282022%29_logo.svg',
      stadium_lat: 51.475944,
      stadium_lng: -0.221914,
    },
    {
      team_name: 'Sunderland',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/7/7b/Sunderland_AFC.svg',
      stadium_lat: 54.914737,
      stadium_lng: -1.388149,
    },
    {
      team_name: 'Crystal Palace',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/a/a2/Crystal_Palace_FC_logo.svg',
      stadium_lat: 51.398338,
      stadium_lng: -0.086084,
    },
    {
      team_name: 'Brentford',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_logo.svg',
      stadium_lat: 51.490715,
      stadium_lng: -0.289048,
    },
    {
      team_name: 'Newcastle United',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/5/5e/Newcastle_United_FC.svg',
      stadium_lat: 54.975711,
      stadium_lng: -1.62162,
    },
    {
      team_name: 'Leeds',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/5/58/Leeds_United_F.C._logo.svg',
      stadium_lat: 53.777353,
      stadium_lng: -1.572778,
    },
    {
      team_name: 'Brighton',
      team_logo:
        'https://w1.pngwing.com/pngs/331/651/png-transparent-premier-league-logo-brighton-organization-brighton-hove-albion-fc-blue-text-line-area-thumbnail.png',
      stadium_lat: 50.861822,
      stadium_lng: -0.083278,
    },
    {
      team_name: 'Wolverhampton Wanderers',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg',
      stadium_lat: 52.590382,
      stadium_lng: -2.130924,
    },
    {
      team_name: 'Liverpool',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg',
      stadium_lat: 53.43083,
      stadium_lng: -2.96083,
    },
    {
      team_name: 'West Ham',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg',
      stadium_lat: 51.538811,
      stadium_lng: -0.017136,
    },
    {
      team_name: 'Manchester City',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_logo.svg',
      stadium_lat: 53.483135,
      stadium_lng: -2.200941,
    },
    {
      team_name: 'Chelsea',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg',
      stadium_lat: 51.481834,
      stadium_lng: -0.19139,
    },
    {
      team_name: 'Manchester United',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg',
      stadium_lat: 53.463493,
      stadium_lng: -2.292279,
    },
    {
      team_name: 'Nottingham Forest',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/e/e5/Nottingham_Forest_F.C._logo.svg',
      stadium_lat: 52.941234,
      stadium_lng: -1.150457,
    },
    {
      team_name: 'Arsenal',
      team_logo:
        'https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg',
      stadium_lat: 51.5549,
      stadium_lng: -0.1084,
    },
  ])
}
