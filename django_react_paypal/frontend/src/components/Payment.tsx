import { PayPalButtons } from "@paypal/react-paypal-js";
import toast from "react-hot-toast";

export function Payment() {
    return (
        <div className="card">
            <img src="https://pbs.twimg.com/profile_images/1250761380271132678/uyRriVUh_400x400.jpg" alt="Prometeo API" style={{ width: '100%' }} />
            <div className="card-details">
                <h1>Prometeo API</h1>
                <p className="price">$10.00</p>
                <p>API's para conectar con bancos</p>
                <PayPalButtons
                   style={{ layout: "horizontal" }}
                   createOrder={(data, actions) => {
                       return actions.order.create({
                           purchase_units: [
                               {
                                   amount: {
                                       value: "10.00",
                                   },
                                   custom_id: "prometeo-api-2022"
                               },
                           ],
                       });
                   }}
                   onCancel={() => toast(
                      "You cancelled the payment. Try again by clicking the PayPal button",
                      {
                          duration: 6000
                      }
                  )}
                  onError={(err) => {
                      toast.error("There was an error processing your payment. If this error please contact support.", { duration: 6000 });
                      }
                  }
                  onApprove={(data, actions) => {
                      return actions.order!.capture().then(function (details) {
                          toast.success('Payment completed. Thank you, ' + details.payer.name!.given_name)
                      });
                  }}
               />
            </div>
        </div>
    )
}
