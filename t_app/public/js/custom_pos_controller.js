frappe.provide("t_app.PointOfSale");

t_app.PointOfSale.Controller = class CustomPOSController extends erpnext.PointOfSale.Controller {
  constructor(wrapper) {
    super(wrapper);
    this.init_tailwind();
  }

  init_tailwind() {
    // Main POS container with gradient background
    this.$wrapper
      .addClass('point-of-sale-app grid grid-cols-10 gap-md bg-gradient-primary min-h-[45rem] h-[calc(100vh-200px)] max-h-[calc(100vh-200px)]');
    // Override Frappe styles
    this.$wrapper.find('.frappe-control').addClass('m-0 !w-full');
    this.$wrapper.find('.form-group').addClass('mb-0');
    // Initialize main sections
    this.$wrapper.html(`
      <div class="items-selector pos-card col-span-6 flex flex-col overflow-hidden bg-white/80">
        <div class="filter-section grid grid-cols-12 bg-success/20 p-lg pb-sm items-center">
          <div class="label col-span-4 pb-xs text-lg font-bold flex items-center text-dark">Items</div>
          <div class="search-field col-span-5 flex items-center mx-sm bg-white rounded-md p-sm border border-secondary/30"></div>
          <div class="item-group-field col-span-3 flex items-center bg-white rounded-md p-sm border border-secondary/30"></div>
        </div>
        <div class="items-container"></div>
      </div>
      <div class="customer-cart-container col-span-4 flex flex-col">
        <div class="customer-section pos-card flex flex-col p-md px-lg bg-white/80"></div>
        <div class="cart-container pos-card flex flex-col items-center mt-md relative h-full bg-white/80">
          <div class="abs-cart-container absolute flex flex-col p-lg w-full h-full">
            <div class="cart-label label pb-md text-dark">Cart</div>
            <div class="cart-items-section"></div>
            <div class="cart-totals-section flex flex-col flex-shrink-0 w-full mt-md">
              <div class="net-total-container flex items-center justify-between p-sm text-md font-medium text-dark bg-success/10 rounded-md"></div>
              <div class="grand-total-container flex items-center justify-between p-sm text-lg font-bold text-dark bg-success/10 rounded-md"></div>
              <div class="checkout-btn primary-action">Checkout</div>
            </div>
          </div>
        </div>
      </div>
    `);
    this.$items_container = this.$wrapper.find('.items-container');
    this.$customer_container = this.$wrapper.find('.customer-section');
    this.$cart_container = this.$wrapper.find('.cart-items-section');
  }

  render_items() {
    this.$items_container
      .empty()
      .addClass('grid grid-cols-4 gap-lg p-lg pt-xs overflow-y-scroll bg-white/50');
    // Use actual item data
    this.items = this.items || this.get_items() || [
      { item_name: 'Item 1', image: '', price_list_rate: 10, description: 'Desc 1' },
      { item_name: 'Item 2', image: '', price_list_rate: 20, description: 'Desc 2' },
    ];
    this.items.forEach(item => {
      this.$items_container.append(`
        <div class="item-wrapper">
          <div class="item-qty-pill absolute flex justify-end m-sm right-0 bg-accent text-dark rounded-full px-2 py-1 text-sm"></div>
          <div class="item-display flex items-center justify-center rounded-md min-h-32 h-32 text-dark m-sm mb-0 bg-white/80">
            <img src="${item.image || ''}" class="image" />
          </div>
          <div class="item-detail flex flex-col justify-center min-h-14 h-14 px-sm bg-white/80 rounded-b-md">
            <div class="item-name nowrap flex items-center text-md text-dark">${item.item_name}</div>
            <div class="item-rate font-bold text-primary">$${item.price_list_rate || 0}</div>
          </div>
        </div>
      `);
    });
  }

  render_customer_section() {
    this.$customer_container
      .empty()
      .addClass('flex flex-col bg-success/20');
    const customer = this.customer || {
      name: 'John Doe',
      image: '',
      desc: 'Regular Customer',
    };
    this.$customer_container.append(`
      <div class="header flex justify-between mb-md pt-md">
        <div class="label text-lg font-bold flex items-center text-dark">Customer</div>
        <div class="close-details-btn flex items-center cursor-pointer text-secondary hover:text-primary">Close</div>
      </div>
      <div class="customer-display flex items-center cursor-pointer bg-white/80 rounded-md p-sm">
        <div class="customer-image flex items-center justify-center w-12 h-12 rounded-full text-dark mr-md bg-accent/30">
          <img src="${customer.image || ''}" class="image rounded-full" />
        </div>
        <div class="customer-name-desc nowrap flex flex-col mr-auto">
          <div class="customer-name font-bold text-lg text-dark">${customer.name}</div>
          <div class="customer-desc text-dark font-medium text-sm">${customer.desc}</div>
        </div>
        <div class="reset-customer-btn flex items-center cursor-pointer text-secondary hover:text-primary">Reset</div>
      </div>
    `);
  }

  render_cart() {
    this.$cart_container
      .empty()
      .addClass('flex flex-col flex-1 overflow-y-scroll bg-white/50');
    this.cart_items = this.cart_items || this.cart || [
      { item_name: 'Item 1', image: '', qty: 2, rate: 10, amount: 20, description: 'Desc 1' },
    ];
    if (this.cart_items.length === 0) {
      this.$cart_container.append(`
        <div class="no-item-wrapper flex items-center justify-center bg-warning/20 rounded-md text-md font-medium w-full h-full text-dark">
          No items in cart
        </div>
      `);
    } else {
      this.cart_items.forEach(item => {
        this.$cart_container.append(`
          <div class="cart-item-wrapper">
            <div class="item-image flex items-center justify-center w-8 h-8 rounded-md text-dark mr-md bg-accent/30">
              <img src="${item.image || ''}" class="image" />
            </div>
            <div class="item-name-desc nowrap flex flex-col flex-1">
              <div class="item-name font-bold text-dark">${item.item_name}</div>
              <div class="item-desc text-sm text-dark font-medium">${item.description || ''}</div>
            </div>
            <div class="item-qty-rate flex flex-shrink-0 text-right ml-md">
              <div class="item-qty flex items-center mr-lg font-bold text-primary">${item.qty}</div>
              <div class="item-rate-amount flex flex-col text-right">
                <div class="item-rate font-bold text-primary">$${item.rate}</div>
                <div class="item-amount text-md font-semibold text-dark">$${item.amount}</div>
              </div>
            </div>
          </div>
        `);
      });
    }
  }
};