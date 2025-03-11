const UserRegistration = artifacts.require('UserRegistration');
const CampaignRegistration = artifacts.require('CampaignRegistration');
const DonationSystem = artifacts.require('DonationSystem');
const PaymentSystem = artifacts.require('PaymentSystem');

module.exports = async function (deployer) {
  await deployer.deploy(UserRegistration);
  await deployer.deploy(CampaignRegistration);
  await deployer.deploy(DonationSystem);
  await deployer.deploy(PaymentSystem);
};
