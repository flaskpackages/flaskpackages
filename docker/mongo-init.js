db.createUser({
    user: 'root',
    pwd: 'pass1',
    roles: [
      {
        role: 'dbOwner',
        db: 'flask_db',
      },
    ],
  });