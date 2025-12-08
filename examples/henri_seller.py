"""
Henri (Seller Agent) Example for Marketplace Demo

Shows SecureAgent with marketplace-specific methods.
"""

from crewai_amorce import SecureAgent
from crewai import Tool

def main():
    print("🔐 Henri (Seller Agent) - Marketplace Example\n")
    
    # Define Henri's tools
    inventory_tool = Tool(
        name="inventory_database",
        description="Check product inventory and condition",
        func=lambda product: f"Found: {product}, Condition: Excellent"
    )
    
    pricing_tool = Tool(
        name="pricing_api",
        description="Get real-time market pricing",
        func=lambda product: {"market_price": 500, "min_price": 450}
    )
    
    # Create Henri as SecureAgent
    print("Creating Henri (Seller Agent)...")
    
    henri = SecureAgent(
        role="Electronics Reseller",
        goal="Maximize profit while maintaining 4.8★ rating",
        backstory="Professional refurbisher with 500+ sales",
        tools=[inventory_tool, pricing_tool],
        hitl_required=['confirm_sale', 'issue_refund'],
        verbose=True
    )
    
    print(f"✅ Henri created with ID: {henri.agent_id}\n")
    
    # Simulate marketplace workflow
    print("--- Marketplace Workflow ---\n")
    
    # 1. Receive offer from Sarah
    print("1. Receiving offer from Sarah...")
    offer = {
        'buyer_id': 'agent_sarah_123',
        'product': 'MacBook Pro 2020',
        'price': 500
    }
    print(f"   Offer: ${offer['price']} for {offer['product']}")
    
    # 2. Check buyer reputation
    print("\n2. Checking buyer reputation...")
    # reputation = henri.check_buyer_reputation(offer['buyer_id'])
    print("   Sarah's trust score: 4.9★ (excellent buyer)")
    
    # 3. Calculate profit margin
    print("\n3. Calculating profit margin...")
    margin = henri.calculate_margin(offer['price'])
    print(f"   Profit margin: ${margin:.2f} ({(margin/offer['price']*100):.1f}%)")
    
    # 4. Make counter-offer
    print("\n4. Making counter-offer...")
    counter = henri.counter_offer(
        price=500,
        reasoning="Fair market value, excellent buyer"
    )
    print(f"   Counter-offer: ${counter['price']}")
    print(f"   Reasoning: {counter['reasoning']}")
    print(f"   Signature: {counter['signature'][:50]}...")
    
    # 5. Generate signed receipt
    print("\n5. Generating signed receipt...")
    receipt = henri.generate_signed_receipt()
    print(f"   Receipt ID: {receipt['timestamp']}")
    print(f"   Seller: {receipt['seller_role']}")
    print(f"   Verified: {receipt['verified_by_amorce']}")
    print(f"   Signature: {receipt['signature'][:50]}...")
    
    print("\n✅ Marketplace workflow complete!")

if __name__ == "__main__":
    main()
