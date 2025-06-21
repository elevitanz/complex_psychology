function [ths0, SEN, SPC, ACC] = thsopt(y, prob)
    Tlist = 0.001:0.001:0.9;
    dista = zeros(length(Tlist), 1);
    
    for j = 1:length(Tlist)
        ths = Tlist(j);
        
        VP = length(find(prob(find(y > 1)) > ths));
        VN = length(find(prob(find(y == 1)) < ths));
        FN = length(find(prob(find(y > 1)) < ths));
        FP = length(find(prob(find(y == 1)) > ths));
        
        % Sensitivity
        if (VP + FN) == 0
            VPR = 0; % avoid division by zero
        else
            VPR = VP / (VP + FN);
        end
        
        % False positive rate (FPR)
        if (FP + VN) == 0
            FPR = 0; % avoid division by zero
        else
            FPR = FP / (FP + VN);
        end
        
        SPC = 1 - FPR; % Specificity
        
        % Store FPR and Sensitivity for plotting or further analysis
        xc(j) = FPR;
        yc(j) = VPR;
        dista(j) = FPR^2 + (1 - VPR)^2;
    end
    
    % Find optimal threshold (ths0)
    ths0 = Tlist(min(find(dista == min(dista))));
    
    % Recompute metrics with the optimal threshold
    VP = length(find(prob(find(y > 1)) > ths0));
    VN = length(find(prob(find(y == 1)) < ths0));
    FN = length(find(prob(find(y > 1)) < ths0));
    FP = length(find(prob(find(y == 1)) > ths0));
    
    % Sensitivity
    if (VP + FN) == 0
        VPR = 0; % avoid division by zero
    else
        VPR = VP / (VP + FN);
    end
    
    % False positive rate (FPR)
    if (FP + VN) == 0
        FPR = 0; % avoid division by zero
    else
        FPR = FP / (FP + VN);
    end
    
    SEN = VPR;  % Sensitivity
    SPC = 1 - FPR; % Specificity
    
    % Accuracy
    if (VP + FN + FP + VN) == 0
        ACC = 0; % avoid division by zero
    else
        ACC = (VP + VN) / (VP + FN + FP + VN);
    end
end
