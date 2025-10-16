import { PrismaClient, Role } from '@prisma/client';
import bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
  const adminEmail = 'admin@breadbreak.local';
  const adminPassword = 'admin123';

  const existingAdmin = await prisma.user.findUnique({ where: { email: adminEmail } });
  if (!existingAdmin) {
    const passwordHash = await bcrypt.hash(adminPassword, 10);
    await prisma.user.create({
      data: {
        email: adminEmail,
        name: 'Admin',
        passwordHash,
        role: Role.ADMIN,
      },
    });
  }

  const products = [
    { name: 'Sourdough Loaf', description: 'Crusty sourdough bread', priceCents: 600 },
    { name: 'Baguette', description: 'Classic French baguette', priceCents: 350 },
    { name: 'Croissant', description: 'Buttery flaky pastry', priceCents: 300 },
    { name: 'Cinnamon Roll', description: 'Sweet cinnamon swirl', priceCents: 400 },
  ];

  for (const p of products) {
    await prisma.product.upsert({
      where: { name: p.name },
      update: {},
      create: p,
    });
  }

  console.log('Seeded admin and products');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
