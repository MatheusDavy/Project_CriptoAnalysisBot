import { useFieldArray, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { formSchema, defaultValues } from "./types";
import type z from "zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { creteSettings, getSettings, updateSettings } from "http/settings";
import { toast } from "sonner";
import { errors } from "types/errors";
import type { ErrorResponse } from "types/api";
import { useEffect } from "react";

type UseLogicProps = {
  onCancelEdit: () => void
  id?: string
}

export const useLogic = ({ id, onCancelEdit }: UseLogicProps) => {
  const client = useQueryClient();

  const { data, isLoading: isLoadingSetting } = useQuery({
    queryKey: ['setting', id],
    enabled: !!id,
    queryFn: () => getSettings(id!),
  })

  const { mutate: onCreate, isPending: isLoadingCreate } = useMutation({
    mutationFn: creteSettings,
    onSuccess: () => {
      toast.success("Success", {
        description: "Settings was created",
      });
      client.invalidateQueries({ queryKey: ['settings'] })
      onCancelEdit();
      form.reset();
    },
    onError: (e: ErrorResponse) => {
      toast.error("Error", {
        description: errors[e?.error],
      });
    },
  });

  const { mutate: onUpdate, isPending: isLoadingUpdate } = useMutation({
    mutationFn: updateSettings,
    onSuccess: () => {
      toast.success("Success", {
        description: "Settings was created",
      });
      client.invalidateQueries({ queryKey: ['settings'] })
      onCancelEdit();
      form.reset();
    },
    onError: (e: ErrorResponse) => {
      toast.error("Error", {
        description: errors[e?.error],
      });
    },
  });

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues,
  });

  const {
    fields: gainFieldArray,
    append: appendGain,
    remove: removeGain,
  } = useFieldArray({
    control: form.control,
    name: "gain_target",
  });

  const {
    fields: lossFieldArray,
    append: appendLoss,
    remove: removeLoss,
  } = useFieldArray({
    control: form.control,
    name: "loss_target",
  });

  const onSubmit = (values: z.infer<typeof formSchema>) => {
    if (!id) onCreate(values);
    else onUpdate({ id, ...values});
  };

  useEffect(() => {
    if (data) {
      form.reset({
        ...data,
        gain_target: data.gain_target,
        loss_target: data.loss_target,
      })
    }
  }, [data])

  return {
    form,
    gainFieldArray,
    lossFieldArray,
    isLoadingCreate,
    isLoadingSetting,
    isLoadingUpdate,
    methods: {
      onSubmit,
      appendGain,
      appendLoss,
      removeGain,
      removeLoss
    },
  };
};
