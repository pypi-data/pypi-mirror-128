import gc
import time
import numpy as np
import torch
from tqdm import tqdm

class PyTorchTraining:
    def train_one_epoch(
            self,
            model, 
            device, 
            loader, 
            optimizer,
            input_formater,
            loss_func, 
            acc_func,
            callback
        ):
        
        gc.collect()
        torch.cuda.empty_cache()
        
        # training begin event
        callback.on_train_begin()
        
        ### Local Parameters
        epoch_loss = []
        epoch_acc = []
        start_time = time.time()

        # Iterating over data loader
        for ii, (data, label, _, body_part) in tqdm(enumerate(loader)):
            # On bach begin
            callback.on_train_batch_begin()
            
            inputs = input_formater.format_data(data)
            target = input_formater.format_label(label)
            
            # Reseting Gradients
            optimizer.zero_grad()
            
            # Forward
            preds = model(inputs)
            
            callback.on_train_loss_begin()
            
            # Calculating Loss
            loss = loss_func.loss(preds, target)
            epoch_loss.append(loss_func.get_loss())
            
            # Calculating Accuracy
            epoch_acc.append(acc_func.get_acc(preds, target))
            
            # Backward
            loss.backward()
            
            callback.on_train_loss_end()
            
            # Optimizer step begin event
            callback.on_step_begin()
            
            optimizer.step()
            
            # Optimizer step end event
            callback.on_step_end()
            
            # On bach end
            callback.on_train_batch_end()
        
        # Overall Epoch Results
        end_time = time.time()
        total_time = end_time - start_time
        
        # Acc and Loss
        epoch_loss = np.mean(epoch_loss)
        epoch_acc = np.mean(epoch_acc)
        
        # Training begin event
        callback.on_train_end()
            
        return epoch_loss, epoch_acc, total_time
    
    def val_one_epoch(
            self,
            model,
            device,
            loader,
            input_formater,
            loss_func, 
            acc_func, 
            callback
        ):

        # Validation begin event
        callback.on_val_begin()                
        
        # Local Parameters
        epoch_loss = []
        epoch_acc = []
        start_time = time.time()
        
        # Iterating over data loader
        for ii, (data, label, _, body_part) in tqdm(enumerate(loader)):
            # On bach start
            callback.on_val_batch_begin()
            
            # Loading images and labels to device
            inputs = input_formater.format_data(data)
            target = input_formater.format_label(label)
            
            # Forward
            preds = model(inputs)
            
            callback.on_val_loss_begin()
            
            # Calculating Loss
            loss_func.loss(preds, target)
            epoch_loss.append(loss_func.get_loss())
            
            # Calculating Accuracy
            epoch_acc.append(acc_func.get_acc(preds, target))
            
            callback.on_val_loss_end()
            
            # On bach end
            callback.on_val_batch_end()
        
        # Overall Epoch Results
        end_time = time.time()
        total_time = end_time - start_time
        
        # Acc and Loss
        epoch_loss = np.mean(epoch_loss)
        epoch_acc = np.mean(epoch_acc)
        
        # epoch end event
        callback.on_val_end()
            
        return epoch_loss, epoch_acc, total_time

    def train_model(
            self,
            model,
            device,
            epochs,
            train_data_loader,
            val_data_loader,
            optimizer_creator,
            scheduler_creator,
            input_formater,
            train_loss_func,
            val_loss_func,
            train_acc_func,
            val_acc_func,
            callback
        ):
        try:
            # On start
            callback.on_start()

            # Loading model to device
            model.to(device)

            for epoch in range(epochs):
                callback.on_epoch_begin()

                model.train()
                optimizer = optimizer_creator.create(model)
                
                # Training
                train_loss, train_acc, train_time = self.train_one_epoch(
                    model=model,
                    device=device,
                    loader=train_data_loader,
                    optimizer=optimizer,
                    input_formater=input_formater,
                    loss_func=train_loss_func,
                    acc_func=train_acc_func,
                    callback=callback
                )

                # Print Epoch Details
                print("\nTraining")
                print("Epoch {}".format(epoch+1))
                print("Loss : {}".format(round(train_loss, 4)))
                print("Acc : {}".format(round(train_acc, 4)))
                print("Time : {}".format(round(train_time, 4)))

                gc.collect()
                torch.cuda.empty_cache()

                # Validation
                print("\nValidating")
                with torch.no_grad():
                    model.eval()
                    val_loss, val_acc, val_time, = self.val_one_epoch(
                        model=model,
                        device=device,
                        loader=val_data_loader,
                        input_formater=input_formater,
                        loss_func=val_loss_func,
                        acc_func=val_acc_func,
                        callback=callback
                    )
                    #Print Epoch Details
                    print("Epoch {}".format(epoch+1))
                    print("Loss : {}".format(round(val_loss, 4)))
                    print("Acc : {}".format(round(val_acc, 4)))
                    print("Time : {}".format(round(val_time, 4)))
                
                # On Epoch End
                callback.on_epoch_end(train_acc, train_loss, train_time, val_acc, val_loss, val_time)
                
                # On Model Saving
                callback.on_model_saving(model, val_acc)

            # On end
            callback.on_end()
        except Exception as e:
            # On Failed
            callback.failed(str(e))
            print(e)